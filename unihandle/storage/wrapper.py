"""
File: __wrapper.py
Author: Kathryn M Phillips (Berbless)
Created: 25.03.25 | DD.MM.YY
Description: Simple function wrapper class for use in UniHandle.
"""

from inspect import ismethod

class UniWrap:
    """
    Function item for use in UniHandle. Holds a function and it's description. 
    """
    __function = lambda: None
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
            err_st = f"ArgErr {len(args)}/{len(self)}:{', '.join(args)} | '{self.__key}:{self}'"
            raise ValueError(err_st)

        # set args locally
        self.__args = args

    def key(self):
        """ return the key (value to run)""" 
        return self.__key