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
        self.id =str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def __str__(self):
        """String Representation of the BaseModel Class"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Updates the attribute 'updated_at' with the current datetime"""
        self.update_at = datetime.now()

    def todict(self):
        """Method to convert BaseModel class to dict"""
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        return (new_dict)
