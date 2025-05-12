"""
Title: Uni(versal) Handle(r) / UniHandle
Author: Kathryn Phillips
Created: 25.03.25 | DD.MM.YY
Version: 0.4.8 (12.05.25) | DD.MM.YY
Description: Simple universal args and menu tool for executing python functions.
"""

from copy import copy
import inspect
import sys

class UniWrap:
    """
    Function item for use in UniHandle. Holds a function and it's description. 
    """
    __function = None
    __args = None
    __key = ""

    def __init__(self, func, key=""):
        """Wrap a function, give it a description and a key name. Executes args() on call."""
        # function to execute (no current option for optional perams).
        self.__function = func
        # Set the key
        self.__key = key

    def __len__(self):
        """Return the quantity of args."""
        count = self.__function.__code__.co_argcount
        if inspect.ismethod(self.__function):
            count -= 1
        return count

    def len(self):
        """Return the quantity of args."""
        return len(self)

    def __str__(self):
        """Return function description"""
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
            output = ""

        # return the output
        return output

    def try_set_args(self, args):
        """
        Instert a list of args into the function. Returns True if valid.
        args: List
        """
        output = ""

        # if the right amount, set args locally
        if len(args) == len(self):
            self.__args = args
            output = ""
        else:
            output = f"ArgErr {len(args)}/{len(self)}:{", ".join(args)} | '{self.__key}:{self}'"

        # return if successfull
        return output

    def key(self):
        """ return the key (value to run)""" 
        return self.__key


class UniHandle:
    """Universal args and menu tool."""
    # Stored items/functions
    __options_dict = {}

    # Keep the program running
    __keep_running = True

    # error codes
    __ERR_INVAL_KEY = -1
    __ERR_INVAL_DICT = -2
    __ERR_INVAL_ARGS = -3
    __ERR_INCMP_ARGS = -4


    def __init__(self, keep_open = False):
        """
        keepOpen: boolean - decides if a close command is needed.
        """
        self.__keep_running = keep_open
        # manually add the exit command
        self.__options_dict["exit"] = UniWrap(self.exit, "exit")


    def __call__(self, args=None):
        """Initialises and runs proccess."""
        # try catch wrapper for keyboard interupts
        try:
            # call sys args, and hand it through to program.
            input_args = sys.argv[1::]

            while self.__keep_running:
                # args to do
                if not input_args is None and input_args != [] and input_args != ['']:
                    # run first args
                    self.__execute_funcs(input_args)
                else:
                    # print options
                    print(self)
                if self.__keep_running:
                    # get user input
                    input_args = self.__proccess_text(input("> "))

            # Run once to just pass initial args through, no menu-ing.
            self.__execute_funcs(input_args)
        # If interupted with keyboard, just, exit.
        except KeyboardInterrupt:
            print("")
            self.__execute_funcs(["exit"])


    def exit(self):
        """Exit after all queued commands."""
        self.__keep_running = False
        return "Exit queued."


    def add(self, key, function):
        """Add a new option to execute (key: callable, func: executable, decr: readable)"""
        # add a new item to the dict
        self.__options_dict[key] = UniWrap(function, key)


    def __setitem__(self, key, function):
        """Add a new option to execute | [key] = (func, decription)"""
        self.__options_dict[key] = UniWrap(function, key)


    def __getitem__(self, key):
        return self.__options_dict[key]


    def __proccess_text(self, text):
        # split on space, unless between " ", or with \ before.
        # ignore \ if \\, then convert to litteral.
        # loop until proccessed.
        special_char = False
        is_brackets = False
        output_array = [""]

        # for all chars of the input
        for char in text:
            # if prev char is an escape char
            if special_char:
                # append
                output_array[-1] += char
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
            elif char == " " and not is_brackets:
                # add a new entry
                output_array.append("")
            # if none of the above, it is just a regular char, or in brackets
            else:
                # append to the last item in the list
                output_array[-1] += char
        return output_array

    def __try_key(self, args):
        # get func 'word'
        word = args[0]

        # return value
        func = None

        # Do basic validation testing
        if not self.__options_dict.keys().__contains__(word):
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
        func = ""
        # that functions args
        func_args = []
        # list of functions to perform in order
        func_list = []
        # Is the current processing valid
        is_valid = True

        # while there are still args to process
        while len(args) > 0 and not func is None:
            # try to pull the func
            func = self.__try_key(args)

            # if it came through right
            is_valid = not func is None

            if is_valid:
                # remove the next
                args.pop(0)

                # while the next is not a word to execute
                while len(args) > 0 and not self.__options_dict.keys().__contains__(args[0]):
                    # remove the next arg and add it to the list of args connected to the func
                    func_args.append(args.pop(0))

                # if not enough values left have been given, raise issue.
                func_set = func.try_set_args(func_args)
                if func_set == "":
                    # if they are, reset func args list (as .
                    func_args = []
                else:
                    # print off what happened
                    print(func_set)
                    # Set out to false
                    is_valid = False
                    func_list = None

                # big rewrite,etc
                if is_valid:
                    # add the packed func to the list to be executed
                    func_list.append(func)
            else:
                # Error exit value
                func_list = None

        # return the packed list
        return func_list


    def __execute_funcs(self, args):
        # generate a list of functions with the args attributed to each.
        packed_functions = self.__compile_funcs(args)

        if not packed_functions is None:
            for func in packed_functions:
                # Else, perform the opperation with name before.
                print(f"{func.key()}:    ", end="")

                # perform func, print output
                print(func())


    def __return_key_string(self, key):
        return f"{key}:   {self.__options_dict[key]}"


    def __str__(self):
        """Return the stored values as a text block \\n seperated."""
        # Form each key into a formatted structure
        # Return every key and description
        key_set = self.__options_dict.keys()
        return "\n".join([self.__return_key_string(key) for key in key_set])

def fish(test):
    """fish | test function"""
    print(test)
    return "THIS IS A TEST"

# Default main func starter.
if __name__ == "__main__":
    handle = UniHandle(keep_open=True)
    # Method: handle[key] = function
    handle["fish"] = fish
    handle()
