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

    def __init__(self, *args, **kwargs):
        """Initializes User Object"""
        super().__init__()
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

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
        """Reset user account password """
        pass

    def change_password(self, new_password):
        """Change the user's password.
        If password is same as default password and password is not
        provided as an argument, prompt user to provide new password

        New password is hashed with sha256 encoding for security.
        """
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        self.password = hashed_password
