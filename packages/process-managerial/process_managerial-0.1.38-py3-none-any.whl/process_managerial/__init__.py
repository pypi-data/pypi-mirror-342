"""
Package: process_managerial

Description:
    This package provides an asynchronous queue system to execute functions in a background worker thread.
    It includes the QueueSystem module for managing tasks and the toolbox module for utility functions.
"""

from .QueueSystem import QueueSystemLite, QueueStatus, FunctionPropertiesStruct

__all__ = [
    "QueueSystemLite",
    "QueueStatus",
    "FunctionPropertiesStruct",
]
