"""
Title: Uni(versal) Handle(r) / UniHandle
Author: Kathryn Phillips
Created: 25.03.25 | DD.MM.YY
Version: 0.4.8 (12.05.25) | DD.MM.YY
Description: Simple universal args and menu tool for executing python functions.
"""

from copy import copy
import inspect
from dsa_double_list import DSALinkedListDouble
from dsa_hash_table import DSAHashTable

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
        # TODO: Optional flags, how?
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
        output = True

        # if the right amount, set args locally
        if len(args) == len(self):
            self.__args = args
        else:
            print(f"ArgErr {len(args)}/{len(self)}:{", ".join(args)} | '{self.__key}:{self}'")
            output = False

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

    def __init__(self, keep_open = False):
        """
        keepOpen: boolean - decides if a close command is needed.
        """
        self.__keep_running = keep_open
        # manually add the exit command
        self.__options_dict["exit"] = UniWrap(self.exit, "exit")


    def __call__(self):
        """Initialises and runs proccess."""
        raw_args = ""
        seperated_args = DSALinkedListDouble()
        compiled_funcs = DSALinkedListDouble()

        # try catch wrapper for keyboard interupts
        try:
            # print options
            print(self)

            while self.__keep_running:
                # get user input
                raw_args = input("> ")
                # If nothing hath been given
                if raw_args == "":
                    # print options
                    print(self)
                else:
                    # convert the input string into args
                    seperated_args = self.__proccess_text(raw_args)
                    # generate a list of functions with the args attributed to each.
                    compiled_funcs = self.__compile_funcs(seperated_args)
                    # send these coalated args into the exectution func
                    self.__execute_funcs(compiled_funcs)
        except KeyboardInterrupt:
            # manual exit forced immediately
            print(f"\n{self.exit()}")

    def exit(self):
        """Exit after all queued commands."""
        self.__keep_running = False
        return "Exit queued."


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
        output_list = DSALinkedListDouble()
        last_item = None

        # give the linked list an initial object
        output_list.insert_first("")

        # for all chars of the input
        for char in text:
            # get current last
            last_item = output_list.get_last()
            # if prev char is an escape char
            if special_char:
                # append the text to the last item
                last_item.set_value(last_item.get_value() + char)
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
                output_list.insert_last("")
            # if none of the above, it is just a regular char, or in brackets
            else:
                # append to the last item in the list
                last_item.set_value(last_item.get_value() + char)

        # if the last char is a space, remove it
        if output_list.peek_last() == "":
            output_list.pop_last()
        return output_list

    def __try_key(self, word):
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
        current_function = ""
        # that functions args
        func_args = DSALinkedListDouble()
        # list of functions to perform in order
        func_list = DSALinkedListDouble()

        # while there are still args to process
        while len(args) > 0 and not current_function is None:
            # try to pull the func
            current_function = self.__try_key(args.peek_first())
            # Reset func args
            func_args = DSALinkedListDouble()

            if current_function is not None:
                # remove the next
                args.pop_first()

                # while the next is not a word to execute
                while len(args) > 0 and not self.__options_dict.keys().__contains__(args.peek_first()):
                    # remove the next arg and add it to the list of args connected to the func
                    func_args.insert_last(args.pop_first())

                # if something went wrong, raise the issue
                if not current_function.try_set_args(func_args):
                    # Set out to false
                    func_list = DSALinkedListDouble()
                    # blank out the func
                    current_function = None
                else:
                    # add the packed func to the list to be executed
                    func_list.insert_last(current_function)
            else:
                # Error exit value
                func_list = DSALinkedListDouble()

        # return the packed list
        return func_list

    def __execute_funcs(self, comiled_funcs):
        # go through the args
        for func in comiled_funcs:
            # Else, perform the opperation with name before.
            print(f"{func.key()}:    ", end="")
            # perform func, print output
            print(func())

    def __str__(self):
        """Return the stored values as a text block \\n seperated."""
        # Form each key into a formatted structure
        # Return every key and description
        key_set = self.__options_dict.keys()
        # get key shortcuts
        out_string = ""
        out_string += "\n<Enter> Show options again"
        out_string += "\n<Ctrl+C> Force quit"
        # get function keys
        for key in key_set:
            out_string += f"\n{key}:   {self.__options_dict[key]}"
        return out_string

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
