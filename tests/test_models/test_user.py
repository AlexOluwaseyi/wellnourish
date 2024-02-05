"""
This module contains the various test for the User to ascertain
the functionality of the model
"""
import unittest
from unittest.mock import patch
from models.user import User
from datetime import datetime
from models.base_model import BaseModel
import hashlib


class TestUser(unittest.TestCase):
    """
    Test Suite for the User Class
    """

    def setUp(self):
        """
        Setup User for testing
        """
        self.user = User()

    def test_is_sub_class(self):
        """
        Test that User is a subclass of BaseModel
        """
        self.assertTrue(isinstance(self.user, BaseModel))

    def test_has_the_expected_attr(self):
        """
        Checks if user has the expected attributes
        """
        self.assertTrue(hasattr(self.user, "id"))
        self.assertTrue(hasattr(self.user, "created_at"))
        self.assertTrue(hasattr(self.user, "updated_at"))
        self.assertTrue(hasattr(self.user, "fname"))
        self.assertTrue(hasattr(self.user, "lname"))
        self.assertTrue(hasattr(self.user, "username"))
        self.assertTrue(hasattr(self.user, "password"))
    
    def test_change_password_with_argument(self):
        self.user.change_password("newpassword")
        hashed_password = hashlib.sha256('newpassword'.encode()).hexdigest()
        self.assertEqual(self.user.password, hashed_password)

    def test_reset_password(self):
        self.user.change_password("newpassword")
        hashed_password = hashlib.sha256('newpassword'.encode()).hexdigest()
        self.assertEqual(self.user.password, hashed_password)
        self.user.reset_password()
        self.assertNotEqual(self.user.password, hashed_password)
        self.assertEqual(self.user.password, self.user.default_password)


if __name__ == '__main__':
    unittest.main()