"""
File: opt_enums.py
Author: Kathryn M Phillips (Berbless)
Created: 30.10.25 | DD.MM.YY
Description: Enum options for startup.
"""

from enum import Enum

class In(Enum):
    NONE = 0
    ARGV = 1
    BOTH = 2
    INPUT = 3

class Out(Enum):
    NONE = 0
    MENU = 1
    ALL = 2