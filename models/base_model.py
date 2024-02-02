#!/usr/bin/python3
"""
BaseModel for WellNourish project.

Keyword arguments:
class BaseModel -- The name of the basemodel class which will be the basics
for all other models, to ease scalability.
"""
from uuid import uuid4
from datetime import datetime

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel():
    """
    BaseModel class definition
    """
    def __init__(self, *args, **kwargs):
        """Initializer for BaseModel class"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.now()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.now()
            if kwargs.get("id", None) is None:
                self.id = str(uuid4())
        else:
            self.id =str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def __str__(self):
        """String Representation of the BaseModel Class"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Method to convert BaseModel class to dict"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        return (new_dict)
