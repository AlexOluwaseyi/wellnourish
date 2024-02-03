#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""
import unittest
from unittest import mock
from models.base_model import BaseModel
from models.user import User
from models.engine.db_storage import DBStorage
import models


class TestDBStorage(unittest.TestCase):
    """
    Test the DBStorage class
    """
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)
        self.assertIs(type(models.storage.all(User)), dict)

    def test_all_with_class(self):
        """Test that all returns a dictionary"""
        users = models.storage.all(User)
        for user in users:
            self.assertTrue(user.password is str)

    def test_new_method(self):
        """Test that all returns a dictionary"""
        user = User()
        models.storage.new(user)
        self.assertIn(user, models.storage._DBStorage__session.new)

    def test_save(self):
        """Test the save method"""
        usr = User()
        models.storage.new(usr)
        models.storage.save()
        user_id = usr.id
        user = models.storage._DBStorage__session.query(User).filter_by(id=user_id).first()
        self.assertIsNotNone(user)

    def test_delete(self):
        """Test the delete method"""
        user = User()
        models.storage.new(user)
        models.storage.save()
        models.storage.delete(user)
        self.assertIn(user, models.storage._DBStorage__session.deleted)
