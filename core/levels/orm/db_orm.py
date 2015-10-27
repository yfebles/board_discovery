# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean, Float, Date, func, and_
from sqlalchemy import create_engine, orm, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from PyQt4.QtGui import QPixmap
import os


Base = declarative_base()

db_path = os.path.join(os.getcwd(), "db")


class ItemTags(Base):
    __tablename__ = 'item_tags'
    item_id = Column(Integer, ForeignKey('Item.item_id'), primary_key=True, nullable=False, autoincrement=True)
    tag_id = Column(Integer, ForeignKey('Tags.tag_id'), primary_key=True, nullable=False)
    distance = Column(Integer, nullable=False)


class Tag(Base):
    """
    The genre of a specie
    """
    # region CONSTANTS
    __tablename__ = 'Tags'
    tag_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    name = Column(String(50), nullable=False, unique=True)
    # endregion

    def __eq__(self, other):
        return isinstance(other, Tag) and self.name == other.name

    def __str__(self):
        return self.name


class Item(Base):
    """
    The family of a specie
    """

    # region CONSTANTS
    __tablename__ = 'Item'
    item_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    descp = Column(String(300))
    image = Column(String(250))
    # tags = relationship(Tag, backref='items', secondary=ItemTags)

    # endregion

    def __eq__(self, other):
        return isinstance(other, Item) and self.name == other.name

    def __str__(self):
        return "name: {0}. id: {1} ".format(self.name, self.item_id)


class Package(Base):

    __tablename__ = 'Package'
    package_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    image = Column(String(50),  nullable=False)
    name = Column(String(50), nullable=False)


class Level(Base):

    __tablename__ = 'Level'
    level_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    package = relationship(Package, backref='levels')
    image = Column(String(50),  nullable=False)
    name = Column(String(50), nullable=False)

    def are_connected(self, i, j):
        """
        return True if the level items at positions i and j are connected
        on the relation matrix
        :param i: index of first item
        :param j: index of second item
        :return:
        """
        if not 0 <= i < len(self.items) or not 0 <= j < len(self.items):
            raise IndexError()

        return i in self.relations[j] or j in self.relations[i]


class Statistics(Base):
    __tablename__ = 'Statistics'
    statistic_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    points = Column(Integer,  nullable=False)
    level = relationship(Level)


class DB:
    """
    DB class that provides a unique connexion into db
    """

    # the engine to request db
    db = create_engine('sqlite:///' + os.path.join(db_path, "db.s3db"), convert_unicode=True)

    # the db session to use to request the db
    _db_session = orm.scoped_session(orm.sessionmaker(bind=db))

    def get_db_session(self, new_session=False):
        """
        Method that returns
        """
        return orm.scoped_session(orm.sessionmaker(bind=self.db)) if new_session else self._db_session
