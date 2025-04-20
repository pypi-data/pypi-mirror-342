import platform
import curses
import os

class AdvancedTextbox:
    """
    This is a replacement for curses.textpad.Textbox() which includes extra
    features:

      1. Arrows can be used to move the cursor left and right
      2. TAB triggers auto-complete based on filesystem paths

    The way to use is different from curses.textpad.Textbox(). Do this:

      1. Create a new curses window
      2. (Optional) draw a rectangle around of it
      3. Create the AdvancedTextbox object.
      4. Call edit() on the AdvancedTextbox object, which will return the
         text that was entered.

    When creating the AdvancedTextbox object, you can pass the following
    arguments:

      1. win: The previously created window where the text input will take place

      2. initial_text: Initial string to put in the edit box.

      3. hints_style: Index in curses.color_pair() that determines the style
         to use in the hints status bar.

      4. autocomplete: If set to False, the TAB key will not autocomplete.

    >>> editwin = curses.newwin(1,curses.COLS-4,2,1)
    >>> curses.textpad.rectangle(stdscr,1,0,1+1+1,1+curses.COLS-4+1)
    >>> textbox = AdvancedTextbox(editwin)
    >>> value = textbox.edit()
    """

    def __init__(self, win, initial_text="", hints_style=0, autocomplete=True):
        self._win           = win
        self._text_backup   = initial_text
        self._text          = initial_text
        self._cursor_pos    = len(initial_text)
        self._hints_style   = hints_style
        self._autocomplete  = autocomplete
        self._hints_window  = curses.newwin(
                                  1,
                                  curses.COLS-1,
                                  curses.LINES-3,
                                  1)
        self._win.keypad(True)


    ############################################################################
    # Internal API
    ############################################################################

    def _display(self):
        self._win.clear()
        self._win.addstr(0, 0, self._text)
        self._win.move(0, self._cursor_pos)
        self._win.refresh()


    def _handle_backspace(self):
        if self._cursor_pos > 0:
            self._text = self._text[:self._cursor_pos - 1] + \
                         self._text[self._cursor_pos:]

            self._cursor_pos -= 1


    def _handle_ctrl_u(self):
        self._text = self._text[self._cursor_pos:]

        self._cursor_pos = 0


    def _handle_ctrl_k(self):
        self._text = self._text[:self._cursor_pos]


    def _move_cursor(self, direction):
        self._cursor_pos = max(0,
                               min(len(self._text),
                                   self._cursor_pos + direction))


    def _insert_char(self, char):
        self._text = self._text[:self._cursor_pos] + \
                     char                        + \
                     self._text[self._cursor_pos:]

        self._cursor_pos += 1


    def _handle_tab(self, consecutive_tabs):

        if not self._autocomplete:
            return

        if self._text:
            aux = self._text[:self._cursor_pos].split()

            if len(aux) == 0:
                current_word = ""
            elif self._cursor_pos > 0 and self._text[self._cursor_pos-1] == " ":
                current_word = ""
            else:
                current_word = self._text[:self._cursor_pos].split()[-1]
        else:
            current_word = ""

        # Get the directory and base name
        #
        dirname, basename = os.path.split(current_word)

        # List files in the directory
        #
        try:
            files = os.listdir(dirname or ".")
        except FileNotFoundError:
            return
        except NotADirectoryError:
            return

        # Filter files that start with the basename
        #
        matches = sorted([f for f in files if f.startswith(basename)])

        if len(matches) == 0:
            return

        elif len(matches) == 1:
            # If there's only one match, complete it
            #
            completed = os.path.join(dirname, matches[0])

        elif len(matches) > 1:
            # If there are multiple matches, complete up to the common prefix
            #
            completed = os.path.join(dirname, os.path.commonprefix(matches))

        if completed[0:2] == "//" and platform.system().upper() == "LINUX":
            # Remote double slash at the beginning (see this:
            # https://stackoverflow.com/questions/52260324/why-os-path-normpath-does-not-remove-the-firsts)
            #
            completed = completed[1:]

        if os.path.isdir(completed) and \
           completed[-1] != "/"     and \
           len(matches)==1:
            completed += "/"

        old_text   = self._text
        self._text = self._text[:self._cursor_pos - len(current_word)] + \
                     completed                                         + \
                     self._text[self._cursor_pos:]

        self._cursor_pos += len(completed) - len(current_word)

        # Show/hide autocomplete hints
        #
        if len(old_text) == len(self._text) and len(matches) > 1:
            # If there are several options to autocomplete, show them on a
            # separate window
            #
            hints_text = " ".join(matches)

            lines, cols = self._hints_window.getmaxyx()

            start = consecutive_tabs*((cols-2)//3)
            end   = start + (cols - 2)

            if end > len(hints_text):
                #start = 0
                #end   = start + (cols - 2)

                consecutive_tabs = 0
            else:
                consecutive_tabs += 1

            hints_text = hints_text[start:end]

            if (len(hints_text) + 3) > cols-2:
                hints_text = hints_text[:cols-2-3] + "..."
            else:
                hints_text += " "*(cols-2-len(hints_text))

            self._hints_window.addstr(0,0,hints_text,
                                      curses.color_pair(
                                          self._hints_style))
        else:
            self._hints_window.clear()
            consecutive_tabs = 0

        self._hints_window.refresh()

        return consecutive_tabs



    ############################################################################
    # Public API
    ############################################################################

    def edit(self):

        consecutive_tabs = 0

        while True:
            self._display()
            key = self._win.getkey()

            if key == "KEY_BACKSPACE":
                self._handle_backspace()
                consecutive_tabs = 0

            elif key == "KEY_LEFT":
                self._move_cursor(-1)
                consecutive_tabs = 0

            elif key == "KEY_RIGHT":
                self._move_cursor(1)
                consecutive_tabs = 0

            elif key == "\t":  # Tab key
                consecutive_tabs = self._handle_tab(consecutive_tabs)

            elif key == "\x15": # Ctrl+U:
                self._handle_ctrl_u()
                consecutive_tabs = 0

            elif key == "\x0b": # Ctrl+K
                self._handle_ctrl_k()
                consecutive_tabs = 0

            elif (key == "KEY_ENTER" or
                  key == "\n"        or
                  key == "\r\n"):
                return self._text

            elif key == "\x1b":            # Escape key
                return self._text_backup

            elif 32 <= ord(key) <= 126:    # Printable characters
                self._insert_char(key)
                consecutive_tabs = 0


class OptionPicker:
    """
    Shows a curses box with several options for the user to select one.
    Up/down arrow keys (and also "j"/"k") are used to change the selection.
    "Enter" or "space" confirm the selection.

    The way to use is this one:

      1. Create a new OptionPicker object.
      2. Call edit() on the OptionPicker object, which will return the newly
         selected option.

    When creating the OptionPicker object, you can pass the following
    arguments:

      1. options: List of strings representing each of the possible options.
         Note that if it is possible to not select any option you need to
         include an empty string in the list.

      2. current: Index from the options list with the currently selected
         option.

    >>> picker = AdvancedTextbox(["", "one", "two", "three"])
    >>> value = picker.edit()
    """

    def __init__(self, options, current, dbg_print):
        self._current        = current
        self._current_backup = current
        self._dbg_print      = dbg_print

        self._rows = min(len(options),
                         curses.LINES-3)
        self._cols = min(max((len(x) for x in options + ["<NONE>",])),
                         curses.COLS-3)

        self._expanded_window = curses.newwin(
                                  self._rows+2,
                                  self._cols+4+1,
                                  (curses.LINES-self._rows)//2-1,
                                  (curses.COLS-self._cols)//2-2)

        self._picker_window   = curses.newwin(
                                  self._rows,
                                  self._cols+1,
                                  (curses.LINES-self._rows)//2,
                                  (curses.COLS-self._cols)//2)

        self._start = 0
        self._stop  = self._rows - 1

        if self._current > self._rows:
            self._start += self._current - self._rows + 1
            self._stop  += self._current - self._rows + 1

        self._options = []
        for o in options:
            if len(o) > self._cols:
                o = o[:-3] + "..." # Truncate if it doesn't fit
            self._options.append(o)


    ############################################################################
    # Internal API
    ############################################################################

    def _display(self):
        self._expanded_window.clear()
        self._picker_window.clear()

        curses.textpad.rectangle(self._expanded_window,
                                 0,0,
                                 self._rows+2-1, self._cols+4-1)

        for i, entry in enumerate(range(self._start, self._stop+1)):

            if entry == self._start and self._start > 0:
                self._picker_window.addstr(i,
                                           self._cols//2 - 1,
                                           "▲ ▲ ▲",
                                           curses.A_DIM)
                continue

            if entry == self._stop and self._stop < len(self._options) - 1:
                self._picker_window.addstr(i,
                                           self._cols//2 - 1,
                                           "▼ ▼ ▼",
                                           curses.A_DIM)
                continue

            txt = self._options[entry] or "<NONE>"
            txt = txt + " "*(self._cols - len(txt))

            if self._current == entry:
                self._picker_window.addstr(i, 0, txt, curses.A_REVERSE)
            else:
                self._picker_window.addstr(i, 0, txt)

        self._expanded_window.refresh()
        self._picker_window.refresh()


    ############################################################################
    # Public API
    ############################################################################

    def edit(self):

        while True:
            self._display()
            key = self._picker_window.getkey()

            if key == "k" or key == "KEY_UP":
                self._current = max(0, self._current-1)
                if self._start > 0:
                    if self._current == self._start:
                        self._start -= 1
                        self._stop  -= 1

            elif key == "j" or key == "KEY_DOWN":
                self._current = min(len(self._options)-1, self._current+1)
                if self._stop < len(self._options) - 1:
                    if self._current == self._stop:
                        self._start += 1
                        self._stop  += 1


            elif (key == "KEY_ENTER" or
                  key == "\n"        or
                  key == "\r\n"):
                return self._options[self._current]

            elif key == "q" or key == "\x1b": # Escape key
                return self._options[self._current_backup]


