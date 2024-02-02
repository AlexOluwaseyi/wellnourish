#!/usr/bin/python3

"""
User Model for all app users
Inherits from BaseModel 

"""

from models.basemodel import BaseModel


class User(BaseModel):
    """
    User class model definition
    """
    def __init__(self, name):
        """Initializer for User class"""
        id = self.id
        name = name.name
        BaseModel.__init__(self)
    