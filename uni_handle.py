"""
Title: Uni(versal) Handle(r) / UniHandle
Author: Kathryn Phillips
Created: 25.03.25 | DD.MM.YY
Version: 0.6.0 (28.09.25) | DD.MM.YY
Description: Simple universal args and menu tool for executing python functions.
"""

from copy import copy
from os import name, system
from inspect import ismethod
from sys import argv

class UniWrap:
    """
    Function item for use in UniHandle. Holds a function and it's description. 
    """
    __function = None
    __args = None
    __key = ""
    __default_output_string = ""

    def __init__(self, func, key=""):
        """Wrap a function, give it a description and a key name. Executes args() on call."""
        # function to execute (no current option for optional perams).
        self.__function = func
        # Set the key
        self.__key = key

    def __len__(self):
        """Return the quantity of args."""
        count = self.__function.__code__.co_argcount
        if ismethod(self.__function):
            count -= 1
        return count

    def len(self):
        """Return the quantity of args."""
        return len(self)

    def __str__(self):
        """Return function description"""
        # get possible docstring.
        output = self.__function.__doc__

        # if the output string will be none, switch it to just blank.
        if output is None:
            output = ""

        # return the output string
        return output

    def __call__(self):
        """
        Execute the stored Function with the stored args.
        """
        # the output value
        output = ""

        # perform func (with args if available)
        if self.__args is not None and len(self.__args) > 0:
            output = self.__function(*self.__args)
        else:
            output = self.__function()

        # if nothing is given use a default string
        if output is None:
            output = self.__default_output_string

        # return the output
        return output

    def set_args(self, args):
        """
        Instert a list of args into the function.
        args: List
        """

        # not the right amount of arguments/perameters
        if len(args) != len(self):
            # raise Value Error.
            raise ValueError(f"ArgErr {len(args)}/{len(self)}:{', '.join(args)} | '{self.__key}:{self}'")

        # set args locally
        self.__args = args

    def key(self):
        """ return the key (value to run)""" 
        return self.__key


class UniHandle:
    """Universal args and menu tool."""
    # Stored items/functions
    __options_dict = None
    # Keep the program running
    __keep_open = True
    # Show hidden/blank functions
    __show_hidden = False
    # turn off the menu
    __no_menu = False
    # Symbol used in command line 'head' -> "> ..."
    __cmd_symbol = "> "

    def __init__(self, keep_open = False, include_predefined = True, show_hidden = False, no_menu = False):
        """
        keep_open:          boolean - decides if a close command is needed.
        include_predefined: boolean - auto set [clear, exit, and "" options]
        show_hidden:        boolean - show functions without docstrings.
        no_menu:            boolean - do not include a menu at all
        """
        # assign the dictionary to prevent pointer sharing hell
        self.__options_dict = {}

        # set default value to the startup flags.
        self.__keep_open = keep_open
        self.__show_hidden = show_hidden
        self.__no_menu = no_menu

        # if a menu is wanted.
        if not no_menu:
            # add hidden show menu options input item.
            self[""] = self.__get_options

        # add the predefined commands
        if include_predefined:
            self["exit"] = self.__exit
            self["clear"] = self.__clear


    def __call__(self):
        """Initialises and runs proccess."""
        # create holder for system args and remove the initial flag (filename)
        sys_inputs = " ".join(argv[1::])

        # try catch wrapper for keyboard interupts
        try:
            # perform the menu loop at least once if has user input.
            self.__menu_loop(sys_inputs)
        except KeyboardInterrupt:
            # exit (and print exit dialog, so it is consistent)
            print(f"\n{self.__exit()}")

    def __menu_loop(self, given_input):
        # input stages
        raw_args = given_input
        seperated_args = []
        compiled_funcs = []

        while self.__keep_open or raw_args != "":
            # convert the input string into args
            seperated_args = self.__proccess_text(raw_args)
            # generate a list of functions with the args attributed to each.
            compiled_funcs = self.__compile_funcs(seperated_args)
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
        # Print off the options when the enter key is pressed
        return str(self)

    def __setitem__(self, key, function):
        """Add a new option to execute | [key] = func"""
        self.__options_dict[key] = UniWrap(function, key)

    def __getitem__(self, key):
        """Return UniWrap Object"""
        return self.__options_dict[key]

    def __proccess_text(self, text):
        # split on space, unless between " ", or with \ before.
        # ignore \ if \\, then convert to 'litteral' (input \ as char).
        # loop until proccessed.
        special_char = False
        is_brackets = False
        output_list = []

        # .strip() to simplify the madness
        text = text.strip()

        # give the linked list an initial object
        output_list.append("")

        # for all chars of the input
        for char in text:
            # if prev char is an escape char
            if special_char:
                # append the text to the last item
                output_list[-1] += char
                # switch back to normal mode
                special_char = False
            # if current char is escape
            elif char == "\\":
                # next can be passed without problem
                special_char = True
            # if current char is 'bracket', switch bracket mode
            elif char == "\"":
                is_brackets = not is_brackets
            # if a space is inserted not in brackets
            elif char == " " and not is_brackets and not output_list[-1] == "":
                # add a new entry
                output_list.append("")
            # if none of the above, it is just a regular char, or in brackets
            elif char != " " or is_brackets:
                # append to the last item in the list
                output_list[-1] += char

        # return the now neatly organised input
        return output_list

    def __get_wrapper(self, word):
        # Check if option is in the dictionary.
        if not word in self.__options_dict:
            raise KeyError(f"{word} is not a valid key.")

        # Check if the option is a functional thing.
        if self.__options_dict[word] is None:
            raise KeyError(f"{word} has invalid entry in Dict.")

        # return UniWrap or None if failed.
        return copy(self.__options_dict[word])


    def __compile_funcs(self, args):
        # the current func
        current_function = ""
        # the current arg
        current_arg = ""
        # that functions args
        func_args = []
        # list of functions to perform in order
        func_list = []

        try:
            # while there are still args to process
            while len(args) > 0:
                # get the next arg
                current_arg = args.pop(0)
                # If the arg is permitted (no_menu isn't enabled.)
                if not(self.__no_menu) or current_arg != "":
                    # pop the next to be tested.
                    current_function = self.__get_wrapper(current_arg)
                    # Reset func args
                    func_args = []

                    # while the next is not a word to execute
                    while len(args) > 0 and not args[0] in self.__options_dict:
                        # remove the next arg and add it to the list of args connected to the func
                        func_args.append(args.pop(0))

                    # add the packed func to the list to be executed
                    current_function.set_args(func_args)
                    func_list.append(current_function)

        # if a problem occurs, skip out, clear to be returned and complain at user (smh).
        except (ValueError, KeyError) as err:
            # print the err
            print(err)
            # Set out to false
            func_list = []

        # return the packed list if successfull
        return func_list

    def __execute_funcs(self, comiled_funcs):
        # go through the args
        for func in comiled_funcs:
            # Else, perform the opperation with name before.
            if func.key() != "":
                print(f"{func.key()}:\n", end="")
            # perform func and print func
            print(func())

    def __str__(self):
        """Return the stored values as a text block \\n seperated."""
        out_string = "\n"
        # get function keys
        for item in self.__options_dict.items():
            # if wants to be printed (has docstring).
            if str(item[1]) != "" or item[0] != "" and self.__show_hidden:
                out_string += f"{item[0]:<7}:{item[1]}\n"
        return out_string

def fish(test):
    """Give a sad fish a name | test function"""
    print(f"TEST FISH: {test}")

# Default main func starter.
if __name__ == "__main__":
    handle = UniHandle(keep_open=True)
    # Method: handle[key] = function
    handle["fish"] = fish
    handle()
