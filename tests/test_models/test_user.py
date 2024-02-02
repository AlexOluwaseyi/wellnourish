"""
This module contains the various test for the User to ascertain
the functionality of the model
"""
import unittest
from models.user import User
from datetime import datetime


class TestUser(unittest.TestCase):
    """
    Test Suite for the User Class
    """

    def setUp(self):
        """
        Setup User for testing
        """
        self.user = User()
