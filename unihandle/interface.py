"""
Title: Uni(versal) Handle(r) / UniHandle
Author: Kathryn M Phillips (Berbless)
Created: 25.03.25 | DD.MM.YY
Description: Simple universal args and menu tool for executing python functions.
"""

from os import name, system
from sys import argv


from .storage import wrap_hold
from .processing import test_processing as proc
from .options.opt_enums import In,Out

class UniHandle:
    """Universal args and menu tool."""
    # The dictionary-like component
    __dic_hold = wrap_hold.WrapHold()
    # input enum
    __in = In.BOTH
    # OutputEnum
    __out = Out.MENU
    # Symbol used in command line 'head' -> "> ..."
    __cmd_symbol = "> "

    def __init__(self, in_opt = In.BOTH, out_opt = Out.MENU):
        """
        in_opt:
            - ARGV => Only take in startup arguments.
            - INPUT => Only take in menu loop options.
            - BOTH => Take in both argv and menu loop.

        out_opt:
            - NONE => Do not include menu entry.
            - MENU => Include menu entry.
            - ALL => Print all items in dictionary through menu.
        """

        # create new wrap_hold
        self.__dic_hold = wrap_hold.WrapHold()

        # set the given option flags.
        self.__in = in_opt
        self.__out = out_opt

        # if a menu is wanted.
        if self.__out != Out.NONE:
            # add hidden show menu options input item.
            self.__dic_hold[""] = self.__get_options

        # add the predefined commands
        self.__dic_hold["exit"] = self.__exit
        self.__dic_hold["clear"] = self.__clear


    def __call__(self):
        """Initialises and runs proccess."""
        # create holder for system args and remove the initial flag (filename)
        sys_inputs = ""

        # if you want to take in argv, do so.
        if not self.__in == In.ARGV:
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

        while self.__in.value > In.ARGV.value or (raw_args != "" and self.__out.value > Out.NONE.value):
            # TODO: CONT HERE
            # convert the input string into args
            seperated_args = proc.proccess_text(raw_args)
            # generate a list of functions with the args attributed to each.
            compiled_funcs = proc.compile_funcs(seperated_args, self.__dic_hold)
            # send these coalated args into the exectution func
            self.__execute_funcs(compiled_funcs)
            # See if still open
            if self.__in.value > In.ARGV.value:
                # get user input
                raw_args = input(self.__cmd_symbol)
            else:
                # clear rem input just in case
                raw_args = ""

    def __exit(self):
        """Exit after all queued commands."""
        self.__in = In.NONE
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
        for item in self.__dic_hold.items(self.__out == Out.ALL):
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
