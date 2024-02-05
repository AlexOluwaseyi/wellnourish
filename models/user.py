#!/usr/bin/python3
"""
User Model for all app users
Inherits from BaseModel
"""

from models.base_model import BaseModel
import hashlib


class User(BaseModel):
    """
    User class model definition
    """
    fname: str = None
    lname: str = None
    email: str = None
    username: str = None
    default_password: str = '1234567890'
    password: str = '1234567890'
    

    def __init__(self, *args, **kwargs):
        """Initializes User Object"""
        super().__init__(*args, **kwargs)
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    """setattr(self, key, value)"""
                    self.fname = kwargs.get("fname", self.fname)
                    self.lname = kwargs.get("lname", self.lname)
                    self.username = kwargs.get("username", self.username)
                    self.email = kwargs.get("email", self.email)
                    self.password = kwargs.get("password", self.password)
    '''
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
                    """
                    self.fname = kwargs.get("fname", self.fname)
                    self.lname = kwargs.get("lname", self.lname)
                    self.username = kwargs.get("username", self.username)
                    self.email = kwargs.get("email", self.email)
                    self.password = kwargs.get("password", self.password)
                    """
    '''

    def get_username(self):
        """Gets the user's username"""
        return self.username
    
    def get_email(self):
        """Gets the user's username"""
        return self.email

    def get_names(self):
        """Gets the user's first name and last name - formatted"""
        return "{} {}".format(self.fname, self.lname)
    
    def reset_password(self):
        """Reset password to default password '1234567890'"""
        self.password = self.default_password

    def change_password(self, new_password):
        """Change the user's password. 
        If password is same as default password and password is not 
        provided as an argument, prompt user to provide new password
        
        New password is hashed with sha256 encoding for security.
        """

        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        self.password = hashed_password
