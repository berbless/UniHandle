"""
Title: Uni(versal) Handle(r) / UniHandle
Author: Kathryn M Phillips (Berbless)
Created: 25.03.25 | DD.MM.YY
Description: Simple universal args and menu tool for executing python functions.
"""

from os import name, system
from sys import argv
from enum import Enum

from .storage import wrap_hold
from .processing import test_processing as proc

class In(Enum):
    pass

class Out(Enum):
    pass

class UniHandle:
    """Universal args and menu tool."""
    # The dictionary-like component
    __dic_hold = wrap_hold.WrapHold()
    # input enum
    In = None
    # OutputEnum
    Out = None
    # Symbol used in command line 'head' -> "> ..."
    __cmd_symbol = "> "

    # Keep the program running
    __keep_open = True
    # Show hidden/blank functions
    __show_hidden = False
    # turn off the menu
    __no_menu = False
    # Do not read argv during parsing
    __ignore_argv = False

    # include_predefined

    # In [ARGV, BOTH, INPUT]
        # keep_open
        # ignore_argv
    # Show [NONE, MENU, ALL]
        # show_hidden
        # no_menu

    def __init__(self,
        keep_open = False,
        include_predefined = True,
        show_hidden = False,
        no_menu = False,
        ignore_argv = False):
        """
        keep_open:          boolean - decides if a close command is needed.
        include_predefined: boolean - auto set [clear, exit, and "" options]
        show_hidden:        boolean - show functions without docstrings.
        no_menu:            boolean - do not include a menu at all
        ignore_argv:        boolean - do not take argv as first call.
        """

        # create new wrap_hold
        self.__dic_hold = wrap_hold.WrapHold()

        # set default value to the startup flags.
        self.__keep_open = keep_open
        self.__show_hidden = show_hidden
        self.__no_menu = no_menu
        self.__ignore_argv = ignore_argv

        # if a menu is wanted.
        if not no_menu:
            # add hidden show menu options input item.
            self.__dic_hold[""] = self.__get_options

        # add the predefined commands
        if include_predefined:
            self.__dic_hold["exit"] = self.__exit
            self.__dic_hold["clear"] = self.__clear


    def __call__(self):
        """Initialises and runs proccess."""
        # create holder for system args and remove the initial flag (filename)
        sys_inputs = ""

        # if you want to take in argv, do so.
        if not self.__ignore_argv:
            sys_inputs = " ".join(argv[1::])

        # try catch wrapper for keyboard interupts
        try:
            # perform the menu loop at least once if has user input.
            self.__menu_loop(sys_inputs)
        except KeyboardInterrupt:
            # exit
            print("\nExiting immediately.")

    def __setitem__(self, key, function):
        """Add a new option to execute | [key] = func"""
        # else, add/replace the entry
        self.__dic_hold[key] = function

    def __getitem__(self, key):
        """Return UniWrap Object"""
        return self.__dic_hold[key]

    def __menu_loop(self, given_input):
        # input stages
        raw_args = given_input
        seperated_args = []
        compiled_funcs = []

        while self.__keep_open or (not self.__no_menu and raw_args != ""):
            # convert the input string into args
            seperated_args = proc.proccess_text(raw_args)
            # generate a list of functions with the args attributed to each.
            compiled_funcs = proc.compile_funcs(seperated_args, self.__dic_hold)
            # send these coalated args into the exectution func
            self.__execute_funcs(compiled_funcs)
            # try if needs to close
            if self.__keep_open:
                # get user input
                raw_args = input(self.__cmd_symbol)
            else:
                # clear rem input just in case
                raw_args = ""

    def __exit(self):
        """Exit after all queued commands."""
        self.__keep_open = False
        return "Exit queued."

    # Source (01.06.25) https://www.geeksforgeeks.org/clear-screen-python/
    def __clear(self):
        """Clear the terminal."""
        # windows support
        if name == "nt":
            system("cls")
        # Linux / MacOS support
        elif name == "posix":
            system("clear")
        else:
            # If not one of the three, strange things have happened.
            # You're on your own.
            print(f"OS ({name}) is not yet supported.")

    def __get_options(self):
        """Return the stored values as a text block \\n seperated."""
        out_string = "\n"
        # get function keys
        for item in self.__dic_hold.items(show_hidden = self.__show_hidden):
            # print the gained ones out.
            out_string += f"{item[0]:<7}:{item[1]}\n"
        return out_string

    def __execute_funcs(self, comiled_funcs):
        # go through the args
        for func in comiled_funcs:
            # Else, perform the opperation with name before.
            if func.key() != "":
                print(f"{func.key()}:\n", end="")
            # perform func and print func
            print(func())
