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
        self.id =str(uuid4)
        self.created_at = datetime.now
        self.updated_at = datetime.now

    def todict(self):
        """Method to convert BaseModel class to dict"""
        return {
            'id' : self.id, 
            'created_at' : self.created_at,
            'updated_at' : self.updated_at
        }
