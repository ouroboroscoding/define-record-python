# coding=utf8
"""Define Record

Define Record data structures
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-21"

# Limit imports
__all__ = ['Data', 'exceptions', 'Storage']

# Local modules
from . import exceptions
from .data import Data
from .storage import Storage