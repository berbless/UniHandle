"""
file: dict_type.py
Author: Kathryn M Phillips (Berbless)
Created: 30.10.25 | DD.MM.YY
Description: The dictionary backbone behind unihandle. Performs the actual dict parts.
"""

from .wrapper import UniWrap
from copy import copy

class WrapHold:
    # Stored items/functions
    __options_dict = {}

    def __init__(self):
        # assign the dictionary to prevent pointer sharing hell
        self.__options_dict = {}

    def __setitem__(self, key, function):
        """Add a new option to execute | [key] = func"""
        # if you are removing something (giving null to it)
        if function is None:
            # pop it off
            self.__options_dict.pop(key)
        else:
            # else, add/replace the entry
            self.__options_dict[key] = UniWrap(function, key)

    def __getitem__(self, key):
        """Return UniWrap Object"""
        return self.__options_dict[key]
    
    def __contains__(self, item):
        return item in self.__options_dict
    
    def __not_desc_less(self, tupl):
        """Return if either part of the tuple is not an empty string"""
        return tupl[0] != "" and tupl[1] != ""

    def items(self, show_hidden = False):
        """Return the items in the dict"""
        output = self.__options_dict.items()

        # if hidden items are not to be included.
        if not show_hidden:
            output = filter(self.__not_desc_less, output)

        return output

    def get(self, word):
        # Check if option is in the dictionary.
        if not word in self.__options_dict:
            raise KeyError(f"{word} is not a valid key.")

        # Check if the option is a functional thing.
        if self.__options_dict[word] is None:
            raise KeyError(f"{word} has invalid entry in Dict.")

        # return UniWrap or None if failed.
        return copy(self.__options_dict[word])