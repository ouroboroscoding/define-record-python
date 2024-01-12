# coding=utf8
"""Record Exceptions

Holds exceptions types throwable by the module
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-26"

class RecordDuplicate(Exception):
	"""Record Duplicate

	Raised when a record is added/saved and it conflicts with an existing record

	Extends:
		Exception
	"""
	pass

class RecordServerException(Exception):
	"""Record Server Exception

	Raised when there's some issue reading or writing from the underlying data \
	server

	Extends:
		Exception
	"""
	pass

class RecordStorageException(Exception):
	"""Record Storage Exception

	Raises when there is some faulure in setting up or configuring the Storage \
	instance

	Extends:
		Exception
	"""
	pass