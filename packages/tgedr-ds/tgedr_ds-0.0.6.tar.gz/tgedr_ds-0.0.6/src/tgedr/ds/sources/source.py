"""
Module Name: source
Description: source-like constructs for data processing
Author:
Date:
Version:

Dependencies:
- ...

Environment Variables:
- ...

Usage:
    >>> from tgedr.ds.sources.source import Source
    >>> class RedditSrc(Source):
    >>> ...

"""
import abc
import os
from typing import Any, Dict, Optional


class SourceException(Exception):
    """
    Exception class for generic exceptions
    """


class NoSourceException(SourceException):
    """
    Exception class for exceptions related with missing data source
    """


# pylint: disable=too-few-public-methods
class SourceInterface(metaclass=abc.ABCMeta):
    """
    def get(self, context: Optional[Dict[str, Any]] = None) -> Any:
        raise NotImplementedError()
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "get") and callable(subclass.get) or NotImplemented


# pylint: disable=too-few-public-methods
@SourceInterface.register
class Source(abc.ABC):
    """
    abstract class defining a method 'get' to manage retrieval of data
    from somewhere as defined by
    implementing classes
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self._config = config

    @abc.abstractmethod
    def get(self, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        gets data

        Args:
            context (dict): must be documented on what parameters must be provided
        Returns:
            data, desirably in a  dataframe format

        Raises:
            eventuallly SourceException, NoSourceException

        """
        raise NotImplementedError()

    def _get_param(
        self,
        key: str,
        context: Optional[Dict[str, Any]] = None,
        default: Optional[Any] = None,
    ) -> Any:
        value = None
        if context is not None:
            value = context.get(key)
        if value is None:
            value = os.environ.get(key)
        if value is None:
            if default is not None:
                value = default
            else:
                raise ValueError(
                    f"""{key} parameter not found neither in environment 
                    nor in provided configuration"""
                )
        return value
