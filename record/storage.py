# coding=utf8
"""Record Storage

Extends the Tree class to add storage capabilities for Records
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-21"

# Limit imports
__all__ = ['CONFLICT', 'Storage']

# Ouroboros imports
from define import Tree
import undefined

# Python imports
import abc
from typing import Literal

# Local imports
from record.data import Data

# Types
CONFLICT = Literal['error', 'ignore', 'replace']

class Storage(Tree, abc.ABC):
	"""Storage

	Represents the top level definition of some sort of stored record

	Extends define.Tree in order to add the ability to validate and clean up \
	data in the record

	Extends:
		define.Tree
	"""

	def __init__(self,
		details: dict | str,
		extend: dict | Literal[False] = undefined,
		key_name: str = '_id'
	):
		"""Constructor

		Initialises the instance

		Arguments:
			details (dict | str): Definition or filepath to load
			extend (dict | False): Optional, a dictionary to extend the \
				definition
			key_name (str): Optional, the name of the primary key field, \
				defaults to '_id'

		Raises:
			KeyError, ValueError

		Returns:
			Storage
		"""

		# Call the parent constructor
		super(Storage, self).__init__(details, extend)

		# Store the key name
		self._key: str = key_name

	@abc.abstractmethod
	def add(self,
		value: dict,
		conflict: CONFLICT = 'error',
		revision_info: dict = undefined
	) -> str | list:
		"""Add

		Adds one raw record to the storage system

		Arguments:
			value (dict): A dictionary of fields to data
			conflict (CONFLICT): A string describing what to do in the case of \
				a conflict in adding the record
			revision_info (dict): Optional, additional information to store \
				with the revision record

		Returns:
			The ID of the added record
		"""
		pass

	@abc.abstractmethod
	def count(self, filter: dict = None) -> int:
		"""Count

		Returns the count of records, with or without a filter

		Arguments:
			filter (dict): Optional, data to filter the count of records by

		Returns:
			int
		"""
		pass

	@abc.abstractmethod
	def exists(self, _id: str):
		"""Exists

		Returns True if the specified ID is found in the storage system

		Arguments:
			_id (str): The ID to check for

		Returns:
			bool
		"""
		pass

	@abc.abstractmethod
	def fetch(self,
		_id: str | list[str] = None,
		filter: dict = None,
		limit: int | tuple | None = None,
		fields: list[str] = None,
		raw: bool | list[str] = False,
		options: dict = None
	) -> Data | list[Data] | dict | list[dict]:
		"""Fetch

		Gets one, many, or all records from the storage system associated with \
		the class instance through one or more checks against IDs, filters, \
		and limits. Passing no arguments at all will return every record \
		available

		Arguments:
			_id: (str | str[]): The ID or IDs used to get the records
			filter (dict): Data to filter the count of records by
			limit (int | Limit): The limit to set for the fetch
			fields (str[]): A list of the fields to be returned for each record
			raw (bool): If true, dicts are returned instead of Data instances
			options (dict): Custom options processed by the storage system

		Returns:
			Data | Data[] | dict | dict[]
		"""
		pass

	@abc.abstractmethod
	def insert(self, value: dict = {}) -> Data | list:
		"""Insert

		Creates a new data object associated with the Storage instance

		Arguments:
			value (dict): The initial values to set for the record

		Returns:
			Data
		"""
		pass

	@abc.abstractmethod
	def install(self) -> bool:
		"""Install

		Installs or creates the location where the records will be stored and \
		retrieved from

		Returns:
			bool
		"""
		pass

	@abc.abstractmethod
	def remove(self,
		_id: str | list[str] = undefined,
		filter: dict = undefined,
		revision_info = undefined
	) -> int:
		"""Remove

		Removes one or more records from storage by ID or filter, and returns \
		the the record or records removed

		Arguments:
			_id (str): Optional, the ID(s) to remove
			filter (dict): Optional, data to filter what gets deleted
			revision_info (dict): Optional, additional data needed to store a \
				revision record. Is dependant on the 'revision' config value

		Returns:
			dict | dict[]
		"""
		pass

	@abc.abstractmethod
	def revision_add(cls, _id: str, changes: dict) -> bool:
		"""Revision Add

		Adds data to the storage system associated with the record that \
		indicates the changes since the previous add/save

		Arguments:
			_id (str): The ID of the record the change is associated with
			changes (dict): The dictionary of changes to add

		Returns:
			bool
		"""
		pass

	@classmethod
	def revision_generate(cls,
		old: dict | list,
		new: dict | list
	) -> dict | None:
		"""Revision Generate

		Generates the list of changes between two records

		Arguments:
			old (dict | list): Old record
			new (dict | list): New record

		Returns:
			dict | None
		"""

		# If we are dealing with a dict
		if isinstance(old, dict):

			# If the new is not also a dict
			if not isinstance(new, dict):
				return { 'old': old, 'new': new }

			# Both are dicts, create a new dict to return
			dRet = {}

			# Get the length of keys in old
			iOldLen = len(old.keys())

			# Store the keys from new and get the length
			lNewKeys = list(new.keys())
			iNewLen = len(lNewKeys)

			# Start checking keys from old
			for k in old:

				# If the key doesn't exist in new
				if k not in new:
					dRet[k] = { 'old': old[k], 'new': None }
					continue

				# It exists in both so pass the two along and remove the key
				#	from the new list
				dTemp = cls.generate_changes(old[k], new[k])
				lNewKeys.remove(k)

				# If there's a value, store it
				if dTemp:
					dRet[k] = dTemp

			# If there's any keys left in the new list
			if lNewKeys:
				for k in lNewKeys:
					dRet[k] = { 'old': None, 'new': new[k] }

			# If the number of keys that are different match the total number of
			#	keys, set everything as changed
			iMaxKeys = iOldLen > iNewLen and iOldLen or iNewLen
			if len(dRet.keys()) >= iMaxKeys:
				return { 'old': old, 'new': new }

			# Return the changes if there are any
			if dRet:
				return dRet

		# Else if we are dealing with a list
		elif isinstance(old, list):

			# If the new is not also a list
			if not isinstance(new, list):
				return { 'old': old, 'new': new }

			# Both are lists, create a new dict to return
			dRet = {}

			# Get the length of the old and new
			iOldLen = len(old)
			iNewLen = len(new)

			# Start going through the indexes of the old
			for i in range(iOldLen):

				# If it's not in the new
				if i >= iNewLen:
					dRet[str(i)] = { 'old': old[i], 'new': None }
					continue

				# It exists in both so pass the two along
				dTemp = cls.generate_changes(old[i], new[i])

				# If there's a value, store it
				if dTemp: dRet[str(i)] = dTemp

			# If there's more new indexes than old
			if iNewLen > iOldLen:
				for i in range(iOldLen, iNewLen):
					dRet[str(i)] = { 'old': None, 'new': new[i] }

			# If the number of indexes different match all data, set everything
			#	as changed
			iMaxKeys = iOldLen > iNewLen and iOldLen or iNewLen
			if len(dRet.keys()) >= iMaxKeys:
				return { 'old': old, 'new': new }

			# Return the changes if there are any
			if dRet: return dRet

		# Else it's a single value
		else:

			# If the new is a dict or list or the values don't match
			if isinstance(new, (dict,list)) or new != old:
				return { 'old': old, 'new': new }

		# No changes
		return None

	@abc.abstractmethod
	def save(self,
		_id: str,
		value: dict,
		replace: bool = False,
		revision_info: dict = undefined,
		full: dict = undefined
	) -> bool:
		"""Save

		Takes existing data and updates it by ID

		Arguments:
			_id (str): The ID of the record to save
			value (dict): A dictionary of fields to data
			replace (bool): Optional, set to True to have the new value \
				overwrite the entire record. Defaults to False
			revision_info (dict): Optional, additional data needed to store a \
				revision record. Is dependant on the 'revision' config value
			full (dict): Optional, the full data, used for revisions and \
				caching, saves processing cycles fetching data from the DB if \
				we already have it

		Returns:
			bool
		"""
		pass

	@abc.abstractmethod
	def uninstall(self) -> bool:
		"""Uninstall

		Uninstalls or deletes the location where the records will be stored \
		and retrieved from

		Returns:
			bool
		"""
		pass