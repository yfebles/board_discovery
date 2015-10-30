# -*- coding: utf-8 -*-
import os
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, mapper


Base = declarative_base()

db_path = "" #os.path.join(os.getcwd(), "core", "levels", "orm")



class ItemLevel(Base):

    __tablename__ = 'item_level'
    item_id = Column(Integer, ForeignKey('Item.item_id'), primary_key=True, nullable=False)
    level_id = Column(Integer, ForeignKey('Level.level_id'), primary_key=True, nullable=False)


class ItemTags(Base):

    __tablename__ = 'item_tags'
    item_id = Column(Integer, ForeignKey('Item.item_id'), primary_key=True, nullable=False)
    tag_id = Column(Integer, ForeignKey('Tags.tag_id'), primary_key=True, nullable=False)
    distance = Column(Integer, nullable=False)


class Tag(Base):

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
    item_id = Column(Integer,  primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    descp = Column(String(300))
    image = Column(String(250))

    tags = orm.relation(Tag, secondary='item_tags',  backref='items')

    # related_items = orm.relation('Item', secondary='item_relation')

    # endregion

    def __eq__(self, other):
        return isinstance(other, Item) and self.name == other.name

    def __str__(self):
        return "name: {0}. id: {1} ".format(self.name, self.item_id)


class Statistics(Base):

    # region CONSTANTS

    __tablename__ = 'Statistics'
    statistics_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    points = Column(Integer, nullable=False, default=0)
    level_id = Column(Integer, ForeignKey('Level.level_id'), nullable=False)

    # endregion


class Level(Base):

    # region CONSTANTS

    __tablename__ = 'Level'
    level_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    image = Column(String(250))
    time_seg = Column(Integer, nullable=False, default=60)
    points = Column(Integer, nullable=False, default=10)
    blocked = Column(Boolean, nullable=False, default=True)
    package_id = Column(Integer, ForeignKey('Package.package_id'), nullable=False)

    items = orm.relation(Item, secondary='item_level',  backref='levels')
    statistic = orm.relation(Statistics, backref='levels')

    # endregion

    def are_connected(self, item1, item2):
        return item2 in item1.related_items or item1 in item2.related_items


class Package(Base):

    # region CONSTANTS

    __tablename__ = 'Package'
    package_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    levels = relationship(Level, backref='package')
    image = Column(String(250))

    # endregion


class ItemRelation(Base):

    __tablename__ = 'item_relation'

    item_id = Column(Integer, ForeignKey('Item.item_id'), primary_key=True, nullable=False)
    item1_id = Column(Integer, ForeignKey('Item.item_id'), primary_key=True, nullable=False)
    descp = Column(String(200), nullable=False)

    items = orm.relation(Item, backref='related_items', primaryjoin=(Item.item_id == item_id))
    items1 = orm.relation(Item, backref='related_items1', primaryjoin=(Item.item_id == item1_id))


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


a = DB().get_db_session()

# for x in a.query(Item).all():
#     for i in x.related_items:
#         print(x.name, )



