#!/usr/bin/python3

"""
BaseModel for WellNourish project.

Keyword arguments:
class BaseModel -- The name of the basemodel class which will be the basics
for all other models, to ease scalability.
"""

from uuid import uuid4
from datetime import datetime

class BaseModel():
    """
    BaseModel class definition
    """
    def __init__(self):
        """Initializer for BaseModel class"""
        id = str(uuid4)
        created_at = datetime.now
        updated_at = datetime.now

    def todict():
        """Method to convert BaseModel class to dict"""
        pass
