# coding=utf8
"""Record Cache

Holds base class used by each individual implementation
"""
from __future__ import annotations

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-08-26"

# Ouroboros imports
import undefined

# Python imports
import abc
from typing import List

class Cache(abc.ABC):
	"""Cache

	Base class that all other Cache implementations must extend from

	Extends:
		abc.ABC
	"""

	__implementations = {}
	"""Classes used to create new cache instances"""

	@classmethod
	def register(cls, implementation: str) -> bool:
		"""Register

		Registers the class `cls` as a type that can be instantiated using the \
		implementation name

		Arguments:
			implementation (str): the name of the implementation that will be \
				added

		Raises:
			ValueError if the name has already been used

		Returns:
			None
		"""

		# If the name already exists
		if implementation in cls.__implementations:
			raise ValueError(implementation, 'already registered')

		# Store the new constructor
		cls.__implementations[implementation] = cls

	@classmethod
	def generate(cls,
		conf: dict
	) -> None | 'Cache':
		"""Generate

		If the enabled flag is set, generates a Cache instance which will be \
		able to fetch and store records by ID. If the flag is not enabled, \
		then None is returned to indicate no caching

		Arguments:
			conf (dict): The configuration for the cache, must contain the

		Raises:
			KeyError if configuration for the implementation is missing
			ValueError if the implementation doesn't exist

		Returns:
			None | Cache
		"""

		print('record: generating "%s"' % conf['implementation'])

		# Get the configuration
		dConf = conf[conf['implementation']]

		# Create the instance by calling the implementation
		try:
			return cls.__implementations[conf['implementation']](dConf)
		except KeyError:
			raise ValueError(conf['implementation'], 'not registered')

	@abc.abstractmethod
	def fetch(self, _id: str | List[str]) -> dict | List[dict]:
		"""Fetch

		Fetches one or more records from the cache. If a record does not \
		exist, None is returned, if the record has previously been marked as \
		missing, False is returned, else the dict of the record is returned. \
		In the case of fetching multiple IDs, a list is returned with the same \
		possible types: False, None, or dict

		Arguments
			_id (str | str[]): One or more IDs to fetch from the cache

		Returns:
			None | False | dict | List[None | False | dict]
		"""
		pass

	@abc.abstractmethod
	def store(self, _id: str, data: dict) -> bool:
		"""Store

		Stores the data under the given ID in the cache

		Arguments
			_id (str): The ID to store the data under
			data (dict): The data to store under the ID

		Returns:
			bool
		"""
		pass

	@abc.abstractmethod
	def add_missing(self, _id: str | List[str], ttl = undefined) -> bool:
		"""Add Missing

		Used to mark one or more IDs as missing from the DB so that they are \
		not constantly fetched over and over

		Arguments:
			_id (str | str[]): The ID(s) of the record that is missing
			ttl (int): Optional, used to set the ttl for this record. By \
				default the ttl used is the same as stored records

		Returns:
			bool | bool[]
		"""
		pass