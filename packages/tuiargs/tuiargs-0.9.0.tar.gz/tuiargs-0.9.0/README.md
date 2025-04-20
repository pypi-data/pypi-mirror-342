# 1. One line description

A library to present all the arguments your script accepts in a TUI (terminal
user interface, using ncurses, that can be navigated with the arrow keys), so
that users can easily figure out what all of them are and do.


# 2. Information for users

## 2.1. Installation

You don't want to use this repository directly. Instead you should "install" the
latest released version by running this command:

    $ python -m pip install tuiargs


## 2.2. User guide

Check [this file](tuiargs/__init__.py) for the full guide.

You can also access this same information from python itself:

    import tuiargs
    
    help(tuiargs)


All public classes and functions are fully documented:

    import tuiargs

    help(tuiargs.Build)
    ...


# 3. Information for developers

## 3.1. Development environment

Make sure you have all python modules listed in "dependencies" section found
inside the pyproject.toml file already installed, if not, use your distro
package manager to install them:

    $ cat pyproject.toml | awk '/dependencies/,/]/' 
    $ pacman -S ...

    NOTE: This (installing dependencies through the global package manager) is
    preferred to creating a virtual environment and using "python -m pip
    install" inside of it because it makes it simpler to run the examples.
    If you insist on using a virtual environment, this is what you need to do:

        $ python -m venv .venv
        $ source .venv/bin/activate
        $ python -m pip install .


Next, update the value of PYTHONPATH to make sure it searches for "tuiargs" in
the current folder (where the source code is) instead of in system paths (in
case you had already "pip install"ed it in the past):

    $ export PYTHONPATH=`pwd`:$PYTHONPATH

You can now run the different included examples like this:

    $ python examples/hello_world.py
    $ python examples/git_wrapper.py


## 3.2. Running the code linter

Before merging new changes you *must* also check that the following command
returns an empty list of warnings:

    $ ruff check .

NOTE: You might need to install "ruff" first. If so, use your distro's package
manager.


## 3.3. Distribution

The source code in this repository is meant to be distributed as a python
package that can be "pip install"ed.

Once you are ready to make a release:

  1. Increase the "version" number in file "pyproject.toml"
  2. Run the next command:

       $ python -m pip install --upgrade build
       $ python -m build

  3. Publish the contents of the "dist" folder to a remote package repository
     such as PyPi (see
     [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/))

  4. Tell your users that a new version is available and that they can install
     it by running this command:

       $ python -m pip install tuiargs

NOTE: If "python -m build" returns an error, you probably have to install the
"python-build" package first, either using your package manager (preferred) or
inside a virtual environment. If you choose the latter, make sure you use the
"--copies" flag when creating the virtual environment or else you will later get
errors about symbolic links when creating the package:

    $ python -m venv --copies .my_venv 

