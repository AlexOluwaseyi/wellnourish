#!/usr/bin/python3
"""
User Model for all app users
Inherits from BaseModel
"""

from flask import session
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String


bcrypt = Bcrypt()


class User(BaseModel, Base, UserMixin):
    """
    User class model definition

    Inherits from BaseModel, Base and UserMixin
    """
    __tablename__ = "users"

    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(128), nullable=False, unique=True)
    username = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    gender = Column(String(8), nullable=True)
    diets = Column(String(128))
    intolerances = Column(String(128))

    def __init__(self, *args, **kwargs):
        """Initializes User Object"""
        super().__init__(*args, **kwargs)
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
                if key == "password":
                    setattr(self, "password",
                            bcrypt.generate_password_hash(value))

    def get_username(self):
        """Gets the user's username"""
        return self.username

    def get_id(self):
        """Gets the user's id"""
        return self.id

    def get_email(self):
        """Gets the user's username"""
        return self.email

    def get_names(self):
        """Gets the user's first name and last name - formatted"""
        return "{} {}".format(self.fname, self.lname)

    def reset_password(self):
        """Reset user account password """
        pass

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def change_password(self, new_password):
        """Change the user's password.
        If password is same as default password and password is not
        provided as an argument, prompt user to provide new password

        New password is hashed with sha256 encoding for security.
        """
        if not new_password:
            raise ValueError("New password cannot be empty")
        self.set_password(new_password)
