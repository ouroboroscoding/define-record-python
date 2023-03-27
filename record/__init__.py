# coding=utf8
"""Define Record

Define Record data structures
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-21"

# Limit imports
__all__ = ['Data', 'Limit', 'Storage']

# Local modules
from . import data, exceptions, storage, types

# Re-Export just the classes/types
Data = data.Data
Limit = types.Limit
RecordDuplicate = exceptions.RecordDuplicate
Storage = storage.Storage