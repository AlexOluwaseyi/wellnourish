#!/usr/bin/python3
"""
User Model for all app users
Inherits from BaseModel
"""

from models.base_model import BaseModel, Base
from uuid import uuid4
import hashlib
import sqlalchemy
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """
    User class model definition
    """
    __tablename__ = "users"

    fname = Column(String(128), nullable=True)
    lname = Column(String(128), nullable=True)
    email = Column(String(128), nullable=False)
    username = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False, default='1234567890')

    fname = None
    lname = None
    email = None
    username= None
    default_password = '1234567890'
    password = '1234567890'

    '''
    def __init__(self, *args, **kwargs):
        """Initializer for User class"""
        super().__init__(*args, **kwargs)
        self.fname = input("Enter First name: ")
        self.lname = input("Enter Last name: ")
        self.username = input("Choose usesrname: ")
        self.email = email
        self.password = password
    '''

    def __init__(self, *args, **kwargs):
        """Initializer for User class"""
        super().__init__(*args, **kwargs)

    def set_username(self, username=None):
        """Sets username for user"""
        if username is not None:
            self.username = username
        else:
            self.username = input("Select a username: ")

    def get_username(self):
        """Gets the user's username"""
        return self.username

    def set_names(self, fname=None, lname=None):
        """Sets the user's names - First Name and Last Name"""
        if fname is not None:
            self.fname = fname
        else:
            self.fname = input("Enter your First name: ")

        if lname is not None:
            self.lname = lname
        else:
            self.lname = input("Enter your Last name: ")

    def get_names(self):
        """Gets the user's first name and last name - formatted"""
        return "{} {}".format(self.fname, self.lname)

    def reset_pasword(self):
        """Reset password to default password '1234567890'"""
        self.password = self.default_password

    def change_password(self, new_password=None):
        """Change the user's password.
        If password is same as default password and password is not
        provided as an argument, prompt user to provide new password
        New password is hashed with sha256 encoding for security."""
        if self.password == self.default_password and new_password == None:
            new_password = input('Enter a new password: ')
        elif self.password != self.default_password and new_password == None:
            new_password = input('Enter a new password: ')
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        self.password = hashed_password
