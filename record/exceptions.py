# coding=utf8
"""Record Exceptions

Holds exceptions types throwable by the module
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-26"

# Limit imports
#__all__ = ['RecordDuplicate']

class RecordDuplicate(Exception):
	"""Record Duplicate

	Raised when a record is added/saved and it conflicts with an existing record

	Extends:
		Exception
	"""
	pass