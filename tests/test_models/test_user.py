"""
This module contains the various test for the User to ascertain
the functionality of the model
"""
import unittest
from models.user import User
from datetime import datetime
from models.base_model import BaseModel


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
