# coding=utf8
"""Record Types

Holds types, classes, named tuples, etc, used by the module
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-26"

# Limit imports
__all__ = ['Limit']

# Python imports
from collections import namedtuple

Limit = namedtuple('Limit', 'start max')
"""Limit

Used to denote the starting point, and max number, of records when fetching them
"""