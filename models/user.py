#!/usr/bin/python3
"""
User Model for all app users
Inherits from BaseModel
"""
from models.base_model import BaseModel


class User(BaseModel):
    """
    User class model definition
    """
    name = ""

    def __init__(self, *args, **kwargs):
        """Initializer for User class"""
        super().__init__(*args, **kwargs)
