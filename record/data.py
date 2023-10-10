# coding=utf8
"""Record Data

Holds data associated with records as well as methods to store that data
"""
from __future__ import annotations

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-26"

# Limit imports
__all__ = ['Data']

# Ouroboros imports
import undefined
from tools import clone, compare, merge

# Python imports
import abc
from copy import copy

# Local imports
import record

# Constants
VALUE_DELETED = {}

class Data(abc.ABC):
	"""Data

	Represents record data
	"""

	def __init__(self, storage: record.Storage, value: dict = {}):
		"""Constructor

		Creates a new instance

		Arguments:
			storage (Storage): The storage class associated with the data
		"""

		# Init the module variables
		self._errors = None
		self._overwrite = False

		# Set the storage class
		self._storage = storage

		# Set the initial value
		self._value = value

		# The record of the specific data that has changed
		self._changes = None

	def __call__(self, default = None):
		"""Call

		Returns the full value stored in the data or the default if there's \
		nothing

		Arguments:
			default (any): Returned if the doesn't exist or is empty

		Returns:
			any
		"""

		# If there's no value
		if self._value is None:
			return default

		# Return a copy of the data
		return clone(self._value)

	def __contains__(self, key):
		"""Contains

		Overrides python magic method __contains__ to check if a key exists in \
		a dictionary like object

		Arguments:
			key (str): The key to check for

		Returns:
			bool
		"""
		return key in self._value

	def __getattr__(self, name: str) -> any:
		"""Get Attribute

		Implements Python magic method __getattr__ to give object notation \
		access to the value. Returns a copy of the value, updating any data \
		returned by accessing values in this way will not affect the instance \
		or any saving

		Arguments:
			name (str): The value key to get

		Raises:
			AttributeError

		Returns:
			any
		"""
		try:
			return copy(self._value[name])
		except KeyError:
			raise AttributeError(name, '%s not in Data' % name)

	def __getitem__(self, name: str) -> any:
		"""Get Item

		Implements Python magic method __getitem__ to give dict access to the \
		value. Returns a copy of the value, updating any data returned by \
		accessing values in this way will not affect the instance or any saving

		Arguments:
			name (str): The value key to get

		Raises:
			AttributeError

		Returns:
			any
		"""
		return copy(self._value[name])

	def __repr__(self) -> str:
		"""Represent

		Overrides python magic method __repr__ to print a string that would \
		compile as returning the instance

		Returns:
			str
		"""
		return '%s(%s, %s)' % (
			self.__class__.__name__,
			self._storage.__repr__(),
			str(self._value)
		)

	def __str__(self) -> str:
		"""String

		Overrides python magic method __str__ to return a string representing \
		the data of the instance

		Returns:
			str
		"""
		return str(self._value)

	def add(self,
		conflict: record.CONFLICT = 'error',
		revision: dict = undefined
	) -> str:
		"""Add

		Adds the record data to the storage system

		Arguments:
			conflict (CONFLICT): A string describing what to do in the case of \
				a conflict in adding the record

		Raises:
			RecordDuplicate

		Returns:
			The ID of the new record
		"""

		# Add the record and store the ID
		self._value[self._storage._key] = self._storage.add(
			self._value,
			conflict,
			revision
		)

		# Clear changes and other flags
		self._changes = None
		self._errors = None
		self._overwrite = False

		# Return the ID
		return self._value[self._storage._key]

	def changed(self) -> bool:
		"""Changed

		Returns whether the data has been changed at all

		Returns:
			bool
		"""
		return self._changes and True or False

	def changes(self) -> dict | None:
		"""Changes

		Returns the specific data that has been changed

		Returns:
			dict | None
		"""
		return clone(self._changes)

	def clean(self) -> None:
		"""Clean

		Cleans the instances values. Be sure to call valid first

		Raises:
			ValueError
		"""

		# Call the clean method on the storage system to clean the data then
		#	use that to overwrite the current value
		self._value = self._storage.clean(self._value)

	@property
	def errors(self) -> list[list[str]]:
		"""Errors

		Read only property that returns the list of errors from the last \
		failed valid call
		"""
		return copy(self._errors)

	def remove(self, revision_info: dict = undefined) -> bool:
		"""Remove

		Removes the existing record data by it's ID

		Arguments:
			revision_info (dict): Optional, additional information to store \
				with the revision record

		Returns:
			True on success
		"""
		return self._storage.remove(
			self._value['_id'],
			revision_info = revision_info
		)

	def save(self, revision_info: dict = None) -> bool:
		"""Save

		Saves the record data over an existing record by ID

		Arguments:
			revision_info (dict): Optional, a dict of additional data needed \
				to add the revision record. Only needed for records that have \
				the revisions flag on

		Raises:
			RecordDuplicate

		Returns:
			True on success
		"""

		# If we are replacing the entire record
		if self._overwrite:

			# Pass the current value to the storage's save method
			result = self._storage.save(
				self._value[self._storage._key],
				self._value,
				True,
				revision_info,
				self._value
			)

		# Else, we are just updating
		else:

			# Pass the changes to the storage's save method
			result = self._storage.save(
				self._value[self._storage._key],
				self._changes,
				False,
				revision_info,
				self._value
			)

		# If we were successful, clear all flags and changes
		if result:
			self._errors = None
			self._changes = None
			self._overwrite = False

		# Return the result
		return result

	def set(self,
		value: dict
	):
		"""Set

		Will completely wipe out the previous value and set the overwrite \
		flag so that any save call will replace the existing record with the \
		new one

		Arguments:
			value (dict): The data to merge with the existing value
			overwrite (bool): Optional, if set to True, all existing data is \
				replaced with the current data
		"""

		# Set the existing value with the new value
		self._value = value

		# Set the overwrite flag, and clear any existing changes
		self._overwrite = True
		self._changes = None

	def __setitem__(self, key: str, value: any):
		"""Set Item

		Uses python magic method to set a fields value using dict notation. \
		Setting values this way completely replaces them. To merge existing \
		values, use the update() method

		Arguments:
			key (str): The key to set
			value (any): The value to set
		"""
		self.__setattr__(key, value)

	def __setattr__(self, name: str, value: any):
		"""Set Attribute

		Uses python magic method to set a fields value using attribute \
		notation. Setting values this way completely replaces them. To merge \
		existing values, use the update() method

		Arguments:
			name (str): The name of the field to set
			value (any): The value to set the field to
		"""

		# If there's no difference, do nothing
		if compare(self._value[name], value):
			return

		# Set the value
		self._value[name] = value

		# Set the overwrite flag, and clear any existing changes
		self._overwrite = True
		self._changes = None

	def update(self, value: dict) -> dict:
		"""Update

		Merges the passed value with the existing data and keeps track of the \
		changes. Will honour any existing overwrite flag so that the merge is \
		with the current value, not the ones originally fetched

		Arguments:
			value (dict): The values to merge over the existing values

		Returns:
			dict | None
		"""

		# Merges the new data with the existing and stores the changes
		dChanges = merge(self._value, value, True)

		# If we have changes
		if dChanges:

			# If we are not already overwriting
			if not self._overwrite:

				# If we have existing changes, merge the new ones onto them
				if self._changes:
					merge(self._changes, dChanges)

				# Else, store the new changes as the changes
				else:
					self._changes = dChanges

		# Return the changes from just this call
		return dChanges

	def valid(self) -> bool:
		"""Valid

		Returns if the currently set values are valid or not

		Returns:
			True if valid
		"""

		# Clear the associated errors
		self._errors = None

		# If we are overwriting
		if self._overwrite:

			# Call the valid method on the storage system to check if the values
			#	we have are ok
			bRes = self._storage.valid(self._value)

		# Else, we are just checking changes
		else:

			# Call the valid method, ignoring any missing nodes, on the storage
			#	system to check if the changes we have are ok
			bRes = self._storage.valid(self._changes, True)

		# If the data isn't valid, store the errors locally and return False
		if bRes is False:
			self._errors = self._storage.validation_failures
			return False

		# Return OK
		return True