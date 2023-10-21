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

	@classmethod
	def factory(cls, conf: dict) -> Cache:
		"""Factory

		Create an instance of the Cache which will be able to fetch and store \
		records by ID

		Arguments:
			conf (dict): The configuration for the cache, must contain the \
				implementation config

		Raises:
			KeyError if configuration for the implementation is missing
			ValueError if the implementation doesn't exist

		Returns:
			Cache
		"""

		# Get the configuration
		dConf = conf[conf['implementation']]

		# Create the instance by calling the implementation
		try:
			return cls.__implementations[conf['implementation']](dConf)
		except KeyError:
			raise ValueError(conf['implementation'], 'not registered')

	@abc.abstractmethod
	def fetch(self,
		_id: str | List[str],
		index = undefined
	) -> None | False | dict | List[None, False, dict]:
		"""Fetch

		Fetches one or more records from the cache. If a record does not \
		exist, None is returned, if the record has previously been marked as \
		missing, False is returned, else the dict of the record is returned. \
		An alternate index can be used to fetch the data, assuming the index \
		is handled by the implementation. In the case of fetching multiple \
		IDs, a list is returned with the same possible types: False, None, or \
		dict

		Arguments:
			_id (str | str[]): One or more IDs to fetch from the cache
			index (str): An alternate index to use to fetch the record

		Returns:
			None | False | dict | List[None | False | dict]
		"""
		pass

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

	@abc.abstractmethod
	def store(self,
		_id: str,
		data: dict,
		indexes = undefined
	) -> bool:
		"""Store

		Stores the data under the given ID in the cache. Also stores \
		additional indexes if passed

		Arguments:
			_id (str): The ID to store the data under
			data (dict): The data to store under the ID
			indexes (dict): Optional, the indexes to store alongside the data

		Returns:
			bool
		"""
		pass