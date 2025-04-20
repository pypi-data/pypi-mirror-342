#!/usr/bin/env python

import os
import re
import copy
import curses
import curses.textpad
import textwrap

from ._internal.components import AdvancedTextbox, OptionPicker


class Build:
    """
    Create an object of this class and then call the run() method to start a
    customized menu-based TUI that will guide the user through all the available
    options.

    Example:

        tui = Build(
              menu_structure,
              ...
        )

        flags = tui.run()

        print(flags)

    This could print something like this:

        ['--debug', '--host', '192.168.10.15', '--', 'output.txt']

    The constructor for objects of this class takes one mandatory parameter
    ("data") and six optional ones for customization:

    @param data:
        List of dictionaries describing the menu tree structure. Each of these
        dictionaries has the following keys:
                       
        - "type":
            Can be "menu", "flag", "option", "positional argument" or "endpoint"

            - "menu" is to embed another list of dictionaries representing
              another menu level. They can be used to model different
              subcommands (ex: "git clone" vs " git diff", "ip link" vs "ip
              route", etc...)

            - "flag" represents an option that can be on or off (it can actually
              also take a counter value, as explained later)

            - "option" and "positional argument" allow the user to type text.
              They accept a "modifier" to specify how this text can be entered:

              - If no modifier is provided, the text is free form.

              - If the ":path" modifier is provided (as in "option:path" and
                "positional argument:path"), then the user will be able to use
                the TAB key to autocomplete (according to the files and folders
                present in the current file system) while typing.

              - If the ":choice:<option1>:<option2>:...:" modifier is provided
                (as in "option:choice:fast:medium:slow" or "positional
                argument:yes:no"), then the user will only be able to enter one
                of the predefined values.

            - "endpoint" is what exits the TUI when selected.
        
        - "label":
            Text label (string) that will be used to display the associated
            entry.
        
        - "description":
            Longer text description (string) that will only be displayed when
            the cursor is over the associated entry.
        
        - "trigger":
            CLI token that is used to "trigger" the  associated entry.

            - When "type" is "flag" or "option", "trigger" must *not* be left
              empty. Example: "--verbose", "-r", "--output-file", ...

              Most of times it will start with "-" or "--", but this is actually
              not enforced.

            - When "type" is "menu" or "endpoint", "trigger" can be left empty
              but typically isn't (at least for "menu"). Example: "commit",
              "encode", ...

              Most of the times this will be a regular word which does not start
              with "-" nor "--", but this is actually not enforced.

            - When "type" is "positional argument", "trigger" has a special
              meaning (a "positional argument" does not have an accompanying
              token and the "type" fields is reused for something else):

              > Most of the times it will be empty and have no effect.

              > If it is not empty it will typically be something like "--".
                This means that the value of the positional argument will only
                appear in the resulting command line *after* (but not
                necessarily immediately after) the provided string.
                This is how it works: if you have several positional arguments
                and all of them set "trigger" to "--", then the resulting
                command line could look like this:

                  --output /tmp -v -- some_file.txt some_other_file.txt
                                      ^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^^^^
                                      positional    positional
                                      argument #1   argument #2

                Note that "--" only appears once in the resulting command line.
        
        - "value":
            - For "menu" it is another list of dictionaries with the same
              recursive structure.

            - For "flag" is a string that contains two numbers separated by "/",
              like this: "A/B", where...

              - (A) is how many times this flag will be provided on the command
                line by default (the most typical case is just one, but there are
                times when it can be higher, such as the "--verbose" flag in some
                programs which can be given several times to increase the
                verbosity level)

              - (B) is the maximum number of times this value can be provided.

            - For "option" and "positional argument", it can be any any of
              these:

              1. An empty string
              2. A string with the default value
              3. A string that starts with $ and contains the name of an
                 environment variable which value will be used.
              4. (2) followed by a pipe ("|") followed by (3) with no spaces
                 before or after "|". The default value will be that of the
                 referenced environment variable if it is set or (2) otherwise.

            - For "endpoint" it must be left empty.
                       
    @param indent_size
        Number of spaces to indent the next submenu entries

    @param panes_border
        Border size around the virtual panes so that text inside does not
        "touch" the edge of the screen

    @param env_help
        Text to show when an option parameter is configured to take its default
        value from an environment variable (if it is set).
        The "XXX" word in the text will be substituted by the actual name of the
        environment variable.

    @param style
        Foreground and background color of different elements of the TUI
        represented by a dictionary with the following keys:
                       
        - "default"      : style used in most places
        - "enpoint"      : style used in menu entries that run the final command
                           when selected
        - "entry"        : style used in menu entries that have a flag, option
                           or positional argument value associated
        - "banner"       : style used for the banner that shows the command that
                           would be ran if a menu "endpoint" was selected
        - "autocomplete" : style used for showing options when invoking
                           TAB auto-complet

        The value associated to each of these keys must be another dictionary
        with two entries: "fg" and "bg" for the foreground and background
        colors respectively. They can take any color name (ex: "white", "green",
        "yellow", ...)

    @param xfixes
        Prefix and suffix to use on special menu entries. The structure is a
        dictionary with the following keys:

        - "menu"       : For menu entries
        - "flag_off"   : For a bolean entry that is currently not enabled
        - "flag_on"    : For a bolean entry that is currently enabled
        - "flag_on_x2" : For a bolean entry that is currently enabled twice
        - "flag_on_x3" : For a bolean entry that is currently enabled 3 times
        - "flag_on_x4" : For a bolean entry that is currently enabled 4 times
        - "flag_on_x5" : For a bolean entry that is currently enabled 5 times

        The value associated to each of these keys must be another dictionary
        with two entries: "prefix" and "suffix", which take any string
        (including the empty one). Examples: "[ ]" for "flag_off, "[X]" for
        "flag_on", etc..
        
    @param dbg_print
        Funtion to call the the TUI wants to generate a debug message. It takes
        a single argument (the string to print). Example:

            def log_print(x):
                global log_messages
                log_messages.append(x)

        Notice that you cannot use "print()" as it will corrupt the TUI. That's
        why in the example above, all messages are saved to a buffer which can
        be later printed to stdout once the TUI exits (you need to manually take
        care of this, though).
    """

    def __init__(
        self,

        data,
                           
        indent_size  = 4,

        panes_border = 6,

        env_help     = "If you don't want to manually specify the value of " +\
                       "this parameter each time, set environment variable " +\
                       "'XXX' and its value will automatically be used here.",

        style        = {
                          "default"      : {"fg":"white",   "bg":"black"},
                          "endpoint"     : {"fg":"green",   "bg":"black"},
                          "entry"        : {"fg":"magenta", "bg":"black"},
                          "banner"       : {"fg":"black",   "bg":"yellow"},
                          "autocomplete" : {"fg":"black",   "bg":"green"},
                        },

        xfixes       = {
                         "menu"       : {"prefix" : "",     "suffix" : "..." },
                         "flag_off"   : {"prefix" : "[ ] ", "suffix" : ""},
                         "flag_on"    : {"prefix" : "[X] ", "suffix" : ""},
                         "flag_on_x2" : {"prefix" : "[2] ", "suffix" : ""},
                         "flag_on_x3" : {"prefix" : "[3] ", "suffix" : ""},
                         "flag_on_x4" : {"prefix" : "[4] ", "suffix" : ""},
                         "flag_on_x5" : {"prefix" : "[5] ", "suffix" : ""},
                       },

        dbg_print    = None, 

    ):
        self._data          = copy.deepcopy(data)
        self._indent_size   = indent_size
        self._env_help      = env_help
        self._panes_border  = panes_border
        self._style         = style
        self._xfixes        = xfixes
        self._dbg_print     = dbg_print if dbg_print else lambda *args: None
        self._envs          = {}

        self._qualifier = {
            "menu"       : "x['type'] == 'menu'",
            "endpoint"   : "x['type'] == 'endpoint'",
            "flag_off"   : "x['type'] == 'flag' and x['value'].split('/')[0] == '0'",
            "flag_on"    : "x['type'] == 'flag' and x['value'].split('/')[0] == '1'",
            "flag_on_x2" : "x['type'] == 'flag' and x['value'].split('/')[0] == '2'",
            "flag_on_x3" : "x['type'] == 'flag' and x['value'].split('/')[0] == '3'",
            "flag_on_x4" : "x['type'] == 'flag' and x['value'].split('/')[0] == '4'",
            "flag_on_x5" : "x['type'] == 'flag' and x['value'].split('/')[0] == '5'",
            "entry"      : "x['type'].startswith(('flag', 'option', 'positional argument'))",
        }

        self._color = dict((b,a+1) for a,b in enumerate(style.keys()))

        # Currently selected item.
        # Implemented as a list of numbers representing each selected entry at
        # each level of the tree hierarchy until the selected item is reached.
        #
        self._current_selection = [0]


    ############################################################################
    # Internal API
    ############################################################################

    class _ResizeException(Exception):
        def __init__(self, message):
            self.message = message
            super().__init__(self.message)


    def _traverse(self):
        """
        Return (yield) each of the entries in the menu together with the "path"
        to reach it.

        Example:
            - ({"type" : "menu",  ...}, [0])       # First element
            - ({"type" : "flag",  ...}, [0,2,2,1]) # Element 4 levels deep
        """

        def _traverse(m, path):
            for entry in m:
                yield (entry, path)

                if entry["type"] == "menu":
                    yield from _traverse(entry["value"], path + [0])

                path = path[:-1] + [path[-1]+1]

        return _traverse(self._data, [0])


    def _resulting_command(self):
        """
        Return the list of "tokens" that make up the command that would be
        executed at this point.
        This list is built by traversing the menu tree until the selected item
        is reached, adding each "trigger" (+ associated data) found in the path.
        """

        cmd                  = []
        positional_arguments = {}

        for entry, path in self._traverse():
            selection_divergence = self._how_different_from_selected(path)

            if selection_divergence == "different":
                # Don't print this line
                continue

            if selection_divergence == "almost subpath" and \
                    (entry["type"] == "menu" or entry["type"] == "endpoint"):
                # Don't print this line
                continue

            if entry["type"] == "flag":
                for x in range(int(entry["value"].split("/")[0])):
                    cmd.append(entry["trigger"])

            elif entry["type"].startswith("option") and entry["value"]:
                cmd.append(entry["trigger"])
                if " " in entry["value"]:
                    cmd.append("\"" + entry["value"] + "\"")
                else:
                    cmd.append(entry["value"])

            elif entry["type"].startswith("positional argument") and \
                 entry["value"]:
                if " " in entry["value"]:
                    value = "\"" + entry["value"] + "\""
                else:
                    value = entry["value"]

                if entry["trigger"] not in positional_arguments.keys():
                    positional_arguments[entry["trigger"]] = []

                positional_arguments[entry["trigger"]].append(value)

            elif entry["type"] == "menu" or entry["type"] == "endpoint":
                if entry["trigger"]:
                    cmd.append(entry["trigger"])

        # "positional argument"s always go at the end of the cmd line. First of
        # all, those without a token, then the rest (with their corresponding
        # token in from of them)
        #
        if "" in positional_arguments.keys():
            cmd = cmd + positional_arguments[""]

        for t, v in positional_arguments.items():
            if t == "":
                continue

            cmd.append(t)
            cmd = cmd + v

        return cmd


    def _how_different_from_selected(self, path):
        """
        Return how "different" the provided path is from the currently selected
        item.

        Examples:

            Path           Current selection        Result
            ----------------------------------------------------------
            [0]            [0]                      "equal"
            [3]            [0]                      "almost subpath"
            [3,1]          [0]                      "different"
            [3,1,2]        [3,1,2]                  "equal"
            [3,1]          [3,1,2]                  "subpath"
            [3]            [3,1,2]                  "subpath"
            [3,2]          [3,1,2]                  "almost subpath"
            [1,2]          [3,1,2]                  "different"
            [1]            [3,1,2]                  "almost subpath"
        """

        if path == self._current_selection:
            return "equal"

        elif len(path) < len(self._current_selection) and \
             path == self._current_selection[:len(path)]:
            return "subpath"

        elif len(path) <= len(self._current_selection) and \
             path[:-1] == self._current_selection[:len(path)-1]:
            return "almost subpath"

        else:
            return "different"


    def _process_input(self, key, stdscr):
        """
        Change the currently selected item
        """

        if key == "j" or key == "KEY_DOWN":

            x = self._data
            for i in self._current_selection[:-1]:
                x = x[i]["value"]

            aux = self._current_selection[-1]
            if aux < len(x)-1:
                aux = aux + 1
                self._current_selection = self._current_selection[:-1] + [aux]

        elif key == "k" or key == "KEY_UP":

            aux = self._current_selection[-1]
            if aux > 0:
                aux = aux-1
                self._current_selection = self._current_selection[:-1] + [aux]

        elif (key == "l"         or
              key == "KEY_RIGHT" or
              key == " "         or
              key == "KEY_ENTER" or
              key == "\n"        or
              key == "\r\n"):

            x = self._data
            for i in self._current_selection[:-1]:
                x = x[i]["value"]

            if x[self._current_selection[-1]]["type"] == "endpoint":
                raise Exception("Exit")

            if x[self._current_selection[-1]]["type"] == "menu":
                self._current_selection.append(0)

            elif x[self._current_selection[-1]]["type"] == "flag":
                v, max_v = \
                    [int(x) for 
                        x in x[self._current_selection[-1]]["value"].split("/")]

                v = (v + 1)%(max_v + 1)

                x[self._current_selection[-1]]["value"] = f"{v}/{max_v}"

            elif x[self._current_selection[-1]]["type"].startswith(
                                             ("option", "positional argument")):

                if ":choice" in x[self._current_selection[-1]]["type"]:
                    options = x[self._current_selection[-1]]["type"].split(":")
                    options = options[2:]

                    pickbox = OptionPicker(
                        options,
                        options.index(x[self._current_selection[-1]]["value"]),
                        self._dbg_print
                    )

                    curses.curs_set(0)
                    new_value = pickbox.edit()

                else:
                    autocomplete = ":path" in x[self._current_selection[-1]]["type"]

                    editwin = curses.newwin(1,curses.COLS-4,2,1)
                    curses.textpad.rectangle(stdscr,1,0,1+1+1,1+curses.COLS-4+1)

                    textbox = AdvancedTextbox(
                        editwin, 
                        initial_text = x[self._current_selection[-1]]["value"],
                        hints_style  = self._color["autocomplete"],
                        autocomplete = autocomplete
                    )

                    stdscr.refresh()

                    curses.curs_set(1)
                    new_value = textbox.edit()
                    curses.curs_set(0)

                x[self._current_selection[-1]]["value"] = new_value

        elif (key == "h"             or
              key == "KEY_LEFT"      or
              key == "KEY_DC"        or
              key == "KEY_BACKSPACE" or
              key == "\b"            or
              key == "\x7f"):

            if len(self._current_selection)>1:
                self._current_selection.pop()

        elif key == "KEY_RESIZE":
            raise self._ResizeException("Terminal was resized")

        elif key == "q":
            raise Exception("Quit")

        else:
            self._dbg_print("Unknown key: " + str(key))


    def _draw(self, stdscr, left_pane_geometry, right_pane_geometry):

        try:
            left   = stdscr.subwin(*left_pane_geometry)
            right  = stdscr.subwin(*right_pane_geometry)
            bottom = stdscr.subwin(2,curses.COLS-1,curses.LINES-3,1)

        except Exception:
            self._dbg_print("Windows too small!")
            stdscr.clear()

            try:
                stdscr.addstr(0,0, "Make window bigger!")
            except Exception:
                pass

            return

        # Find number of selected row and, based on that, the needed scroll
        # offset
        #
        selected_row = 0
        for entry, path in self._traverse():
            selection_divergence = self._how_different_from_selected(path)

            if selection_divergence == "different":
                continue

            if selection_divergence == "equal":
                break

            selected_row = selected_row + 2

        if selected_row > left_pane_geometry[0]-1:
            scroll = selected_row - (left_pane_geometry[0]-1)
            if scroll % 2 == 1:
                scroll = scroll+1
        else:
            scroll = 0

        self._dbg_print(f"Selected row = {selected_row} | Scroll offset = {scroll}")

        # Draw entries
        #
        row = 0
        for entry, path in self._traverse():

            selection_divergence = self._how_different_from_selected(path)

            if selection_divergence == "different":
                # Don't print this line
                continue

            label = entry["label"]

            # Add a prefix/suffix to the label to print (if needed)
            #
            for q, v in self._xfixes.items():
                x = entry
                if eval(self._qualifier[q]):
                    label = v["prefix"] + label + v["suffix"]

            # Add colors and other features (if needed)
            #
            if selection_divergence == "equal":
                # This is the currently selected item
                attr = curses.A_BOLD
            else:
                attr = curses.A_DIM

            if entry["type"] == "endpoint":
                attr += curses.A_UNDERLINE

                if selection_divergence == "equal":

                    cmd = " ".join(self._resulting_command())

                    if (len(cmd) + 3) > curses.COLS-2:
                        cmd = cmd[:curses.COLS-2-3] + "..."
                    else:
                        cmd += " "*(curses.COLS-2-len(cmd))

                    bottom.addstr(0, 0, "Arguments:")
                    bottom.addstr(1, 0,
                                  cmd, curses.color_pair(self._color["banner"]))

            for q in self._style.keys():
                if q in ["default", "banner", "autocomplete"]:
                    continue
                if eval(self._qualifier[q]):
                    attr += curses.color_pair(self._color[q])

            # Print label on left pane
            #
            if row < scroll:
                stdscr.addstr(self._panes_border-1,
                              self._panes_border,
                              "▲ ▲ ▲",
                              curses.A_DIM)

            elif (row-scroll) >= left_pane_geometry[0]:
                stdscr.addstr(curses.LINES-self._panes_border,
                              self._panes_border,
                              "▼ ▼ ▼",
                              curses.A_DIM)

            else:
                left.addstr(row-scroll, 
                            self._indent_size*(len(path)-1),
                            label,
                            attr)

                if selection_divergence == "equal":

                    # Clean up the text to show in the right panel so that:
                    #   - Lines are not split in the middle of words
                    #   - Paragraphs are preserved
                    #
                    help_text = []
                    paragraph = []

                    for line in re.split("\n",
                                         textwrap.dedent(entry["description"])):
                        if line:
                            paragraph.append(line)
                        else:
                            help_text.append(textwrap.fill(
                                               " ".join(paragraph),
                                               width = right_pane_geometry[1]-2
                                             ) + "\n\n")

                            paragraph = []

                    if paragraph:
                        help_text.append(textwrap.fill(
                                           " ".join(paragraph),
                                           width = right_pane_geometry[1]-2
                                        ) + "\n\n")

                    # Print the text to show in the right panel
                    #
                    if entry["type"].startswith(("option", 
                                                 "positional argument")):

                        # Try to read the parameter value from an environment
                        # variable (if set)
                        #
                        actual_value = ""
                        for x in entry["value"].split("|"):
                            if x and x[0] == "$":
                                self._envs[str(path)] = x[1:]
                                if os.getenv(x[1:]):
                                    actual_value = os.getenv(x[1:])
                                    break
                            else:
                                actual_value = x

                        entry["value"] = actual_value

                        try:
                            right.addstr(0,   0, "Current value: ")
                            if entry["value"]:
                                right.addstr(0,  16, entry["value"], curses.A_REVERSE)
                            else:
                                right.addstr(0,  16, "<NONE>", curses.A_DIM)
                            right.addstr("\n")
                            right.addstr("\n")
                        except Exception:
                            pass

                    for x in help_text:
                        try: 
                            right.addstr(x)
                        except Exception:
                            pass

                    if str(path) in self._envs.keys():
                        try:
                            right.addstr(textwrap.fill(
                                           self._env_help.replace(
                                               "XXX",
                                               self._envs[str(path)]),
                                           width = right_pane_geometry[1]-2
                                        ), curses.A_BOLD)
                        except Exception:
                            pass

            row = row + 2


    def _loop(self, stdscr):
        """
        Processing loop that takes input and updates the display.
        """

        # Hide cursor
        #
        curses.curs_set(0)

        # Enable arrow keys
        #
        stdscr.keypad(True)

        # Length needed to print the longest line (including intentations and
        # prefixes/suffixes)
        #
        max_col = 0
        for entry, path in self._traverse():
            last_col = self._indent_size*len(path) + len(entry["label"])

            for q, v in self._xfixes.items():

                x = entry # noqa: F841
                          # This might look like an unused variable, but it is
                          # actually being used inside the "eval" in the next
                          # line.

                if eval(self._qualifier[q]):
                    last_col += (len(v["prefix"]) + len(v["suffix"]))

            if last_col > max_col:
                max_col = last_col

        # Size of left and right pane based on screen size, pane borders size
        # and length of longest line
        #
        left_pane_geometry  = (
                curses.LINES - 2*self._panes_border, # height
                max_col,                             # width
                self._panes_border,                  # y_off
                self._panes_border                   # x_off
        )

        right_pane_geometry = (
                curses.LINES - 2*self._panes_border,           # height
                curses.COLS  - 3*self._panes_border - max_col, # width
                self._panes_border,                            # y_off
                2*self._panes_border + max_col                 # x_off
        )

        self._dbg_print(f"left_pane  = {left_pane_geometry}")
        self._dbg_print(f"right_pane = {right_pane_geometry}")

        # Initialize color styles
        #
        for color in self._style.keys():
            curses.init_pair(
                    self._color[color],
                    eval("curses.COLOR_" + self._style[color]["fg"].upper()),
                    eval("curses.COLOR_" + self._style[color]["bg"].upper())
            )

        stdscr.bkgd(self._color["default"])

        # Main loop (draw + process input + draw + ...)
        #
        while True:
            stdscr.clear()

            self._draw(
              stdscr,
              left_pane_geometry,
              right_pane_geometry,
            )

            key = stdscr.getkey()

            try:
                self._process_input(key, stdscr)

            except self._ResizeException:

                new_rows, new_cols = stdscr.getmaxyx()

                if (new_rows, new_cols) != (curses.LINES, curses.COLS):
                    curses.resizeterm(*stdscr.getmaxyx())

                    left_pane_geometry  = (
                            curses.LINES - 2*self._panes_border, # height
                            max_col,                             # width
                            self._panes_border,                  # y_off
                            self._panes_border                   # x_off
                    )

                    right_pane_geometry = (
                            curses.LINES - 2*self._panes_border,           # height
                            curses.COLS  - 3*self._panes_border - max_col, # width
                            self._panes_border,                            # y_off
                            2*self._panes_border + max_col                 # x_off
                    )

                    self._dbg_print("Terminal window was resized!")
                    self._dbg_print(f"left_pane  = {left_pane_geometry}")
                    self._dbg_print(f"right_pane = {right_pane_geometry}")

            stdscr.refresh()


    ############################################################################
    # Public API
    ############################################################################

    def run(self):
        """
        Start the TUI.

        This function will only return once the TUI is stopped which can be
        achieved in two ways:

        - The user presses "q" to quite.
        - The user selects one of the "endpoints" available in the menus
        """

        try:
            curses.wrapper(self._loop)
        except Exception as e:
            if str(e) == "Quit":
                return ""
            elif str(e) == "Exit":
                return self._resulting_command()
            else:
                raise e
