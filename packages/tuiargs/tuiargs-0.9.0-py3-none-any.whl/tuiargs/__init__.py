"""
A library to build TUIs that helps users discover CLI options/arguments


================================================================================
1. OVERVIEW
================================================================================

Some programs tend to have too many command line options/arguments. The worst
offenders are those that contain "subcommands" each of which with their own set
of dedicated options/arguments (example:  "git", "ffmpeg", "ip", ...)

This forces the user to open the man page on one tab and carefully compose the
final command line in another tab while reading through all the different
sections of the documentation... or worse... ask an AI!

This library was created to help with this problem.

Let's say you are developing one of these complex commands with subcommands and
dozens of options/arguments. The idea is that, in addition to the man page, you
would also forge a data structure (a python dictionary) describing all these
options/arguments (type of values they accept, hierarchical relationship among
them, etc...), feed that into this library and let it run, which will have this
effect:

    1. Start a TUI ("terminal user interface") where the user can navigate with
       the arrow keys through all the available arguments/options.

    2. Let the user "investigate" each of them (documentation for the currently
       selected option is printed in real time as he browses all the entries)

    3. Let the user enable/disable and/or set/clear options interactively.

    4. Let the user decide when he is done. At this point the library will
       return an array of ARGVs to your program, just as that received from sys
       in the typical case. Example: ["-l", "--output", "/tmp/file.txt",
       "--verbose"]


================================================================================
2. USAGE
================================================================================

You need to:

    1. Import the library
    2. Create a python dictionary containing your arguments/options structure
    3. Call Build()
    4. Call run()
    5. Process the array of ARGVs returned by run()

Example:

```python
import tuiargs

menu_structure = \
[
  {
    "type"        : "flag",
    "label"       : "Global flag #1",
    "description" : "This is a global flag",
    "trigger"     : "--global-flag-1",
    "value"       : "0/1",
  },
  {
    "type"        : "option",
    "label"       : "Global option",
    "description" : "This is a global option with a default value",
    "trigger"     : "--global-option",
    "value"       : "my default value",
  },
  {
    "type"        : "endpoint",
    "label"       : "Run!",
    "description" : "Select this to exit the TUI",
    "trigger"     : "",
    "value"       : None,
  },
]

tui  = tuiargs.Build(menu_structure)
args = tui.run()

print(args)
```

The format of the python dictionary that Build() takes describing available
options/arguments (as well as all the other optional arguments that let you
customize the look and feel of the TUI) are fully documented in the Build class
itself. You can access this documentation by running this from a python
interpreter:

   >>> import tuiargs
   >>> help (tuiargs.Build)

There are also some more complex examples inside the "examples/" folder included
in the source code distribution of this library. I recommend you read them first
and then execute them like this:

    $ python examples/<name_of_example_file>.py


================================================================================
2. WRAPPERS TO EXISTING TOOLS
================================================================================

Even if you are not the developer of a tool (and/or if that tool is not written
in python) you can still take advantage of this library.

Let's say you want to add the functionality this library provides to "git". One
thing you could do is creating a wrapper called "git_wrapper.py" that would use
this library to collect options/arguments depending on what the user wants and
then, at the end, call the real "git" with the corresponding array of ARGVs.

In fact, something like this is what I try to showcase with file
"examples/git_wrapper.py" (provided with the source code distribution of this
library). It's just an example, far from complete (in fact, it just implements a
bunch of git options), but it's a good start point in case you (or I) even find
the time and will to complete the task :)
"""


from .lib import Build
