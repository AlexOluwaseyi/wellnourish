#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import models
from models.base_model import BaseModel
from models.user import User


class DBStorage:
    """
    Interacts with the a particular database
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the DB storage class"""
        pass

    def all(self, cls=None):
        """Returns object dictionary of the data in database"""
        pass

    def new(self, obj):
        """Add the object to the current database session"""
        pass

    def save(self):
        """Commit all changes of the current database session"""
        pass

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        pass

    def reload(self):
        """Reloads data from the database"""
        pass

    def close(self):
        """Call remove() method on the private session attribute"""
        pass

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        pass
