import tuiargs



################################################################################
## Menu layout
################################################################################

menu_structure = \
[
  {
    "type"        : "flag",
    "label"       : "Global flag #1",
    "description" : """\
                    Here is where the 'real' description of the flag would go.

                    Instead of that let me tell you that this is a global flag
                    which affects all menus below. In general, all flags on a
                    given level will affect all menus and submenus in nested
                    levels.
                    
                    When this option is selected, the '--global-flag-1' flag
                    will be appended to the resulting command line.
                    """,
    "trigger"     : "--global-flag-1",
    "value"       : "0/1",
  },
  {
    "type"        : "flag",
    "label"       : "Global flag #2",
    "description" : """\
                    This is another global flag, the difference with the
                    previous one being that it is enabled by default (which is
                    done by setting the 'value' field to 'True').
                    """,
    "trigger"     : "--global-flag-2",
    "value"       : "1/1",
  },
  {
    "type"        : "flag",
    "label"       : "Global flag #3",
    "description" : """\
                    This is another global flag. This time it can be provided up
                    to 3 times, so every time you select this option the counter
                    will increment until it wraps back to zero.
                    """,
    "trigger"     : "--global-flag-3",
    "value"       : "0/3",
  },
  {
    "type"        : "option",
    "label"       : "Global option",
    "description" : """\
                    This is a global option with a default value of 'my default
                    value'

                    When its value is set to a non empty <string>, the following
                    two flags will be appended to the resulting command line:

                    --global-option <string>

                    If its value is empty, neither of them wil be appended to
                    the resulting command line.
                    """,
    "trigger"     : "--global-option",
    "value"       : "my default value",
  },
  {
    "type"        : "option:path",
    "label"       : "Global option (file autocomplete)",
    "description" : """\
                    This is another global option but it is being set to type
                    "option:path", which means you will be able to use the TAB
                    key when typing its value to autocomplete according to the
                    files present in your file system.
                    """,
    "trigger"     : "--global-option-file",
    "value"       : "",
  },
  {
    "type"        : "option:choice:green:blue:red",
    "label"       : "Global option (pick one)",
    "description" : """\
                    This is another global option but this time there is a
                    predefined set of valid values and you are only allowed to
                    select one of them
                    """,
    "trigger"     : "--global-option-pick",
    "value"       : "blue",
  },
  {
    "type"        : "option:choice::green:blue:red",
    "label"       : "Global option II (pick one)",
    "description" : """\
                    Same as above, but notice how this time we can provide an
                    "empty" value, meaning the option will not be considered
                    (notice the "empty" value contained between the two
                    consecutive "::")
                    """,
    "trigger"     : "--global-option-pick2",
    "value"       : "green",
  },
  {
    "type"        : "positional argument",
    "label"       : "Global positional argument",
    "description" : """\
                    This is a global positional argument.

                    Its value (if set) will be appended *at the end* to the
                    resulting command line.

                    Notice that because we are setting its "trigger" field to
                    "--", that means it (together with all the other positional
                    arguments) will appear after a "--" is automatically
                    inserted in the resuting command line.
                    """,
    "trigger"     : "--",
    "value"       : "",
  },
  {
    "type"        : "menu",
    "label"       : "Menu 1",
    "description" : """\
                    This is the first menu, representing, for example, a
                    "subcommand" of the tool.

                    Menus are containers of more entries (which can also be
                    other menus).

                    In this block of text you would explain what makes this menu
                    different from the other ones (ie. the way this 'subcommand'
                    works)

                    Note that menus also have a 'trigger' field that will be
                    appended to the resulting command line when the menu is
                    selected. You can leave 'trigger' empty if not needed.
                    """,
    "trigger"     : "menu_1",
    "value"       : [
      {
        "type"        : "flag",
        "label"       : "Flag #1",
        "description" : """\
                        This is a flag specific to Menu #1. If the user selects
                        it but then goes 'back' in the menu hierarchy and ends
                        up executing something from inside Menu #2, this option
                        will not appear in the resulting command line.
                        """,
        "trigger"     : "--flag-1",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "Flag #2",
        "description" : """\
                        This is another flag specific to Menu #1. 

                        By the way, notice that when documeting options, you can
                        add spaces at the beginning of each line for indentation
                        purposes (as we have been doing on this file since the
                        beginning).

                        You can also start a new paragraph by adding an empty
                        line (as I just did).
                        """,
        "trigger"     : "--flag-2",
        "value"       : "0/1",
      },
      {
        "type"        : "option",
        "label"       : "Option A for menu #1",
        "description" : """\
                        For multiple choice parameters you define a 'string'
                        (such as this one) and then, in the documentation, you
                        list the options. Example:

                        valid_value_1: if you want to do X

                        valid_value_2: if you want to do Y

                        etc...
                        """,
        "trigger"     : "--local-option-1-a",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Option B for menu #1",
        "description" : """\
                        Another thing about 'string' arguments, is that in the
                        'value' field you can use $SOME_VARIABLE_NAME. This
                        means the value of that environment variable will be
                        used in case it exists and no manual value is entered.

                        When you do this, an explanation will automatically be
                        added to the description (the next paragraph -in bold
                        characters- was automatically added)
                        """,
        "trigger"     : "--local-option-1-b",
        "value"       : "$VALUE_FOR_OPTION_B",
      },
      {
        "type"        : "option",
        "label"       : "Option C for menu #1",
        "description" : """\
                        It is possible to have a default value *and also* an
                        environment variable (which will take precedence) using
                        a '|' symbol.

                        As it was the case before, both the default value and
                        the environment variables will be ignored if a manual
                        value is entered.
                        """,
        "trigger"     : "--local-option-1-c",
        "value"       : "some default value|$VALUE_FOR_OPTION_C",
      },
      {
        "type"        : "endpoint",
        "label"       : "Run!",
        "description" : """\
                        Endpoints are what triggers the generation of the final
                        command line.

                        Before pressing enter you can see a preview of what the
                        final command line will be in the yellow bar at the
                        bottom of the screen.
                        """,
        "trigger"     : "",
        "value"       : None,
       },
    ],
  },
  {
    "type"        : "menu",
    "label"       : "Menu 2",
    "description" : """\
                    This is the second menu, representing, for example, another
                    "subcommand" of the tool.

                    Note that the 'trigger' can be empty (as in this example)
                    and no extra token will be appended to the resulting command
                    line.
                    """,
    "trigger"     : "",
    "value"       : [
      {
        "type"        : "flag",
        "label"       : "Flag #3",
        "description" : """\
                        This is a flag specific to Menu #2.
                        """,
        "trigger"     : "--flag-3",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "Flag #4",
        "description" : """\
                        This is another flag specific to Menu #2. 
                        """,
        "trigger"     : "--flag-4",
        "value"       : "0/1",
      },
      {
        "type"        : "option",
        "label"       : "Option X for menu #2",
        "description" : """\
                        This is an option specific to Menu #2.
                        """,
        "trigger"     : "--local-option-2-x",
        "value"       : "",
      },
      {
        "type"        : "positional argument",
        "label"       : "Positional argument menu #2",
        "description" : """\
                        This is a positional argument specific to Menu #2.

                        It will appear after the other global positional
                        argument (if set) and both of them will appear after a
                        "--" token because that is what their "trigger" field
                        has been set to.
                        """,
        "trigger"     : "--",
        "value"       : "",
      },
      {
        "type"        : "endpoint",
        "label"       : "Run!",
        "description" : """\
                        This is the exit entry for the second menu. 

                        Note that 'trigger' can be non-empty if desired (but
                        typically you will want to leave it empty)
                        """,
        "trigger"     : "--run-menu-2",
        "value"       : None,
       },
    ],
  },
]



################################################################################
## Auxiliary functions
################################################################################

log_messages = []

def log_print(x):
    global log_messages
    log_messages.append(x)



################################################################################
## Main()
################################################################################

tui = tuiargs.Build(
      menu_structure,
      dbg_print = log_print
)

exception = None

try:
    args = tui.run()
except Exception as e:
    exception = e

for x in log_messages:
    print("LOG: " + str(x))
print("")

if exception:
    raise exception

print(f"Arguments: {args}")

