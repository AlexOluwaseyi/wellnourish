#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import os
import models
from models.base_model import BaseModel, Base
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """
    Interacts with the a particular database
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the DB storage class"""
        if os.getenv("WN_ENV") == "test":
            self.__engine = create_engine("sqlite:///test.db")
            Base.metadata.drop_all(self.__engine)
        else:
            self.__engine = create_engine("sqlite:///wellnourish.db")

    def all(self, cls=None):
        """Returns object dictionary of the data in database"""
        all_dict = {}
        if cls is None or cls is User:
            objs = self.__session.query(cls).all()
            for obj in objs:
                if obj and hasattr(obj, 'id'):
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    all_dict[key] = obj
        return (all_dict)

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session

    def close(self):
        """Call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        pass
