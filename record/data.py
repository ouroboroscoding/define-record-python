# coding=utf8
"""Record Data

Holds data associated with records as well as methods to store that data
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-26"

# Limit imports
__all__ = ['Data']

# Python imports
import abc
from copy import copy, deepcopy

# Pip imports
from define import NOT_SET

class Data(abc.ABC):
	"""Data

	Represents record data
	"""

	def __init__(self, storage: callable, value: dict = {}):
		"""Constructor

		Creates a new instance

		Arguments:
			storage (Storage): The storage class associated with the data
		"""

		# Set the storage class
		self._storage = storage

		# Set the initial value
		self._value = value

		# Init the list of fields that have changed
		self._changed = []

	def __delattr__(self, __name: str) -> None:
		return super().__delattr__(__name)

	def __contains__(self, key):
		"""Contains

		Overrides python magic method __contains__ to check if a key exists in a
		dictionary like object

		Arguments:
			key (str): The key to check for

		Returns:
			bool
		"""
		return key in self._value

	def __delattr__(self, name: str) -> None:
		"""Del(ete) Attr(ibute)

		Overrides python magic method __delattr__ for deleting an attribute from
		an object like instance

		Arguments:
			name (str): The attribute to delete

		Raises:
			AttributeError
		"""
		try:
			return self.field_remove(name)
		except KeyError as e:
			raise AttributeError(*e.args)

	def __delitem__(self, key):
		"""Del(ete) Item

		Overrides python magic method __delitem__ for deleting a key from a dict
		like instance

		Arguments:
			key (str): The key to delete

		Raises:
			KeyError
		"""
		self.field_remove(key)

	def __getattr__(self, name: str) -> any:
		"""Get Attr(ibute)

		Overrides python magic method __getattr__ for getting an attribute from
		object like instance

		Arguments:
			name (str): The attribute to return

		Raises:
			AttributeError

		Returns:
			any
		"""
		v = self.field_get(name, NOT_SET)
		if v is NOT_SET:
			raise AttributeError(name)
		return self._value[name]

	def __getitem__(self, key):
		"""Get Item

		Overrides python magic method __getitem__ for getting a key from a dict
		like instance

		Arguments:
			key (str): The key to return

		Raises:
			KeyError

		Returns:
			any
		"""
		v = self.field_get(key, NOT_SET)
		if v is NOT_SET:
			raise KeyError(key)
		return self._value[key]

	def __setattr__(self, name: str, value: any) -> None:
		"""Set Attr(ibute)

		Overrides python magic method __setattr__ for setting an attribute in an
		object like instance

		Arguments:
			name (str): The attribute to set
			value (any): The value of the attribute

		Raises:
			AttributeError
			ValueError
		"""
		try:
			return self.field_set(name, value)
		except KeyError as e:
			raise AttributeError(*e.args)

	def __setitem__(self, key, value):
		"""Set Item

		Overrides python magic method __setitem__ for setting a key in a dict
		like instance

		Arguments:
			key (str): The key to set
			value (any): The value of the key

		Raises:
			KeyError
			ValueError
		"""
		return self.field_set(key, value)

	def __repr__(self) -> str:
		"""Represent

		Overrides python magic method __repr__ to print a string that would
		compile as returning the instance

		Returns:
			str
		"""
		return '%s(%s, %s)' % (
			self.__class__.__name__,
			self._storage.__repr__(),
			str(self._value)
		)

	def __str__(self):
		"""String

		Overrides python magic method __str__ to return a string representing
		the data of the instance

		Returns:
			str
		"""
		return str(self._value)

	@abc.abstractmethod
	def add(self) -> str:
		"""Add

		Adds the record data to the storage system

		Raises:
			RecordDuplicate

		Returns:
			The ID of the new record
		"""
		pass

	@abc.abstractmethod
	def changed(self, field: str) -> bool:
		"""Changed

		Returns whether a specific field has been changed

		Arguments:
			field (str): The field to check for changes

		Returns:
			True if the field has been changed
		"""

		# If the field is in the changed
		if field in self._changed:
			return True

		# If the field is a complex type
		if self[field].class_name() != 'Node':

			# Call the instances changed and return that
			return self[field].changed()

	def changes(self) -> list:
		"""Changes

		Returns the list of fields that have been changed

		Returns:
			list
		"""
		return list(self._changed.keys())

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
	def errors(self) -> list:
		"""Errors

		Read only property that returns the list of errors from the last failed
		valid call
		"""
		return copy(self._errors)

	def field_get(self, field, default=None):
		"""Field Get

		Returns a specific field, if it's not found, returns the default

		Both __getattr__ and __getitem__ use this method to get the field

		Arguments:
			field (str): The field to get
			default (mixed): Returned if the field doesn't exist

		Returns:
			any
		"""

		# If the field doesn't exist
		if field not in self._value:
			return default

		# Return the field
		return self._value[field]

	def field_remove(self, field: str):
		"""Field Remove

		Deletes a specific field from the record value

		Both __delattr__ and __delitem__ use this method to remove the field

		Arguments:
			field (str): The field to remove

		Raises:
			KeyError
			ValueError

		Returns:
			self for chaining
		"""

		# If the field is not valid for the record
		if field not in self._storage:
			raise KeyError(field)

		# If the field doesn't exist in the data there's nothing to do
		if field not in self._value:
			return self

		# Remove the field from the document
		del self._value[field]

		# Flag the field as being changed
		self._changed[field] = True

		# Return self for chaining
		return self

	def field_set(self, field, value):
		"""Field Set

		Sets a specific field in a record

		Both __setattr__ and __setitem__ use this method to set the field

		Arguments:
			field (str): The name of the field to set
			value (any): The value to set the field to

		Raises:
			KeyError: field doesn't exist in the structure of the record
			ValueError: value is not valid for the field

		Returns:
			self for chaining
		"""

		# If the field is not valid for the record
		if field not in self._storage:
			raise KeyError(field)

		# If the field hasn't changed, do nothing
		if field in self._value and value == self._value[field]:
			return self

		# If the value isn't valid for the field
		if not self._storage[field].valid(value, [field]):
			raise ValueError(self._storage[field].validation_failures)

		# If we need to keep changes
		if self._storage.changes:
			if self._old_value is None:
				self._old_value = deepcopy(self._value)

		# If the value is None, store it as is
		if value is None:
			self._value[field] = None

		# Else, store it after cleaning it
		else:
			self._value[field] = self._storage[field].clean(value)

		# Mark the field as changed
		self._changed[field] = True

		# Return self for chaining
		return self

	@abc.abstractmethod
	def remove(self) -> bool:
		"""Remove

		Removes the existing record data by it's ID

		Returns:
			True on success
		"""
		pass

	@abc.abstractmethod
	def save(self) -> bool:
		"""Save

		Saves the record data over an existing record by ID

		Raises:
			RecordDuplicate

		Returns:
			True on success
		"""
		pass

	def valid(self, level = NOT_SET) -> bool:
		"""Valid

		Returns if the currently set values are valid or not

		Returns:
			True if valid
		"""

		# Clear the associated errors
		self._errors = None

		# Call the valid method on the storage system to check if the values we
		#	have are ok. If they aren't, store the errors locally
		if self._storage.valid(self._value) is False:
			self._errors = self._storage.validation_failures
			return False

		# Return OK
		return True

	@property
	def value(self) -> dict:
		"""Value

		Read-only property that returns the current value
		"""
		return copy(self._value)