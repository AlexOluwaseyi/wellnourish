#!/usr/bin/python3
"""
User Model for all app users
Inherits from BaseModel
"""

from models.base_model import BaseModel, Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from passlib.hash import bcrypt
import hashlib
import sqlalchemy
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """
    User class model definition
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(128), nullable=False, unique=True)
    username = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes User Object"""
        super().__init__(*args, **kwargs)
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

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    def change_password(self, new_password):
        """Change the user's password.
        If password is same as default password and password is not
        provided as an argument, prompt user to provide new password

        New password is hashed with sha256 encoding for security.
        """
        if not new_password:
            raise ValueError("New password cannot be empty")
        self.set_password(new_password)
