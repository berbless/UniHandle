"""
Title: Uni(versal) Handle(r) / UniHandle
Author: Kathryn Phillips
Created: 25.03.25 | DD.MM.YY
Version: 0.5.8 (25.07.25) | DD.MM.YY
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
        return self.__function.__doc__

    def get_doc(self):
        """Dirty hack to get if this has a docstring to print."""
        return self.__function.__doc__

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

    def try_set_args(self, args):
        """
        Instert a list of args into the function. Returns True if valid.
        args: List
        """
        output = True

        # if the right amount, set args locally
        if len(args) == len(self):
            self.__args = args
        else:
            print(f"ArgErr {len(args)}/{len(self)}:{', '.join(args)} | '{self.__key}:{self}'")
            output = False

        # return if successfull
        return output

    def key(self):
        """ return the key (value to run)""" 
        return self.__key


class UniHandle:
    """Universal args and menu tool."""
    # Stored items/functions
    __options_dict = None
    # keys in order (since there is no removing keys, should be a-ok)
    __keys = None
    # Keep the program running
    __keep_running = True

    def __init__(self, keep_open = False, include_predefined = True):
        """
        keepOpen: boolean - decides if a close command is needed.
        """
        # assign the objects here to prevent pointer sharing hell
        self.__options_dict = {}
        self.__keys = []

        self.__keep_running = keep_open
        # add the predefined commands
        if include_predefined:
            self["exit"] = self.__exit
            self["clear"] = self.__clear
            self[""] = self.__get_options


    def __call__(self):
        """Initialises and runs proccess."""
        # create holder for system args and remove the initial flag (filename)
        sys_inputs = argv[1::]

        # try catch wrapper for keyboard interupts
        try:
            # If user input is given through sys argv
            if len(sys_inputs) > 0:
                # generate a list of functions with the args attributed to each.
                sys_inputs = self.__compile_funcs(sys_inputs)
                # send these coalated args into the exectution func
                self.__execute_funcs(sys_inputs)
            else:
                # print first menu
                print(self.__get_options())

            # open the menu if need to
            if self.__keep_running:
                # perform the menu loop (if set to do so)
                self.__menu_loop()

        except KeyboardInterrupt:
            # manual exit forced immediately
            print(f"\n{self.__exit()}")

    def __menu_loop(self):
        # input stages
        raw_args = ""
        seperated_args = []
        compiled_funcs = []

        while self.__keep_running:
            # get user input
            raw_args = input("> ")
            # convert the input string into args
            seperated_args = self.__proccess_text(raw_args)
            # generate a list of functions with the args attributed to each.
            compiled_funcs = self.__compile_funcs(seperated_args)
            # send these coalated args into the exectution func
            self.__execute_funcs(compiled_funcs)

    def __exit(self):
        """Exit after all queued commands."""
        self.__keep_running = False
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
        """Add a new option to execute | [key] = (func, decription)"""
        self.__options_dict[key] = UniWrap(function, key)
        self.__keys.append(key)


    def __getitem__(self, key):
        return self.__options_dict[key]


    def __proccess_text(self, text):
        # split on space, unless between " ", or with \ before.
        # ignore \ if \\, then convert to litteral.
        # loop until proccessed.
        special_char = False
        is_brackets = False
        output_list = []

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

        # if the last char is a space (and not just a blank input, remove it
        if len(output_list) > 1 and output_list[-1] == "":
            output_list.pop(-1)
        return output_list

    def __try_key(self, word):
        # return value
        func = None

        # Do basic validation testing
        if not word in self.__options_dict.keys():
            print(f"{word} is not a valid key.")

        elif self.__options_dict[word] is None:
            print(f"{word} has invalid entry in Dict.")

        else:
            # get func
            func = copy(self.__options_dict[word])

        # return func
        return func


    def __compile_funcs(self, args):
        # the current func
        current_function = ""
        # that functions args
        func_args = []
        # list of functions to perform in order
        func_list = []

        # while there are still args to process
        while len(args) > 0 and not current_function is None:
            # try to pull the func
            current_function = self.__try_key(args[0])
            # Reset func args
            func_args = []

            if current_function is not None:
                # remove the next
                args.pop(0)

                # while the next is not a word to execute
                while len(args) > 0 and not (args[0] in self.__options_dict.keys()):
                    # remove the next arg and add it to the list of args connected to the func
                    func_args.append(args.pop(0))

                # if something went wrong, raise the issue
                if not current_function.try_set_args(func_args):
                    # Set out to false
                    func_list = []
                    # blank out the func
                    current_function = None
                else:
                    # add the packed func to the list to be executed
                    func_list.append(current_function)
            else:
                # Error exit value
                func_list = []

        # return the packed list
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
        for key in self.__keys:
            # if wants to be printed (has docstring).
            if self.__options_dict[key].get_doc() is not None:
                out_string += f"{key:<7}:{self.__options_dict[key]}\n"
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
