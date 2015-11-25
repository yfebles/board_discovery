# -*- coding: utf-8 -*-
import os
from sqlalchemy import Column, Integer, ForeignKey, Boolean, Unicode
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, mapper, relation


Base = declarative_base()

# db_path = ""

db_path = os.path.join(os.getcwd(), "core")


class ItemTags(Base):

    __tablename__ = 'item_tags'
    item_id = Column(Integer, ForeignKey('Item.item_id', ondelete='cascade'), primary_key=True, nullable=False)
    tag_id = Column(Integer, ForeignKey('Tags.tag_id', ondelete='cascade'), primary_key=True, nullable=False)

    # the distance at which the tag describes the item (!! lower is more descriptive !!)
    distance = Column(Integer, nullable=False)


class Tag(Base):

    __tablename__ = 'Tags'
    tag_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(Unicode(50), nullable=False, unique=True)

    item_tags = relationship(ItemTags, backref='tag')

    # parent tag
    parent_id = Column(Integer, ForeignKey('Tags.tag_id', ondelete='cascade'), nullable=True)
    children = relation('Tag',  backref=orm.backref("parent", remote_side='Tag.tag_id'))

    def get_distance(self, item):
        """
        get the distance at which the tag is to an item
        :param self:
        :param item_list:
        :return:
        """
        # get the distance (if any) between the self and the item directly (must be >=0 to be valid)
        tag_directly_related = [i.distance for i in item.item_tags if i.tag == self and i.distance >= 0]

        # found a relation valid between self and item (must be unique)
        if len(tag_directly_related) == 1:
            return tag_directly_related[0]

        # try to find the relation between the tags children
        max_distance = -1
        related_tags = [t.tag for t in item.item_tags]
        related_child_tags = [t for t in self.children if t in related_tags]

        for child_tag in related_child_tags:
            distance = child_tag.get_distance(item)

            if distance > 0:
                max_distance = max(max_distance, 1 + distance)

        return max_distance

    def __eq__(self, other):
        return isinstance(other, Tag) and self.name == other.name

    def __str__(self):
        return self.name


class Item(Base):
    """
    The family of a specie
    """

    __tablename__ = 'Item'
    item_id = Column(Integer,  primary_key=True, nullable=False, autoincrement=True)
    name = Column(Unicode(50), nullable=False, unique=True)
    description = Column(Unicode(300))
    image = Column(Unicode(250))

    # items tags
    item_tags = relationship(ItemTags, backref='item')

    def related_by_tag(self, max_distance=-1):
        related_by_tag_list = []

        items_from_tags_to_check = []
        for item_tag1 in self.item_tags:
            if max_distance < 0 or item_tag1.distance < max_distance:
                items_from_tags_to_check.extend(item_tag1.tag.item_tags)

        # get the items related to each of my tags closer that max distance
        for item_tag in items_from_tags_to_check:
            if item_tag.item is None or self == item_tag.item:
                continue

            # the distance of the related item to the tag that is closer to my d
            if max_distance < 0 or item_tag.distance <= max_distance:
                related_by_tag_list.append((item_tag.item, item_tag.distance))

        return related_by_tag_list

    def all_related_items(self, max_distance=0):
        """
        returns the list of all related items and their distance to the current
        """
        by_tag = [x[0] for x in self.related_by_tag(max_distance)]

        return self.directly_related + by_tag

    def distance(self, other):
        """
        Returns the min distance between the current item and one supplied
        """
        if not isinstance(other, Item) or other is None:
            raise Exception()

        if other in self.directly_related:
            return 0

        by_tag = self.related_by_tag()
        founds = [x[1] for x in by_tag if x[0] == other]

        if len(founds) > 0:
            return min(founds)

        return -1

    def __eq__(self, other):
        return isinstance(other, Item) and self.name == other.name

    def __str__(self):
        return u"name: {0}. id: {1} ".format(self.name, self.item_id)


class ItemRelation(Base):
    """
    The relations between items could be through tags that both
    share or by other directly relationship
    """

    __tablename__ = 'item_relation'

    item_id = Column(Integer, ForeignKey('Item.item_id', ondelete='cascade'), primary_key=True, nullable=False)
    item1_id = Column(Integer, ForeignKey('Item.item_id', ondelete='cascade'), primary_key=True, nullable=False)

    descp = Column(Unicode(200), nullable=False)

    items = orm.relation(Item, backref='directly_related', primaryjoin=(Item.item_id == item1_id))
    distance = Column(Integer, nullable=False)


class ItemLevel(Base):
    """
    The item-level belonging relationship
    """
    __tablename__ = 'item_level'
    item_id = Column(Integer, ForeignKey('Item.item_id', ondelete='cascade'), primary_key=True, nullable=False)
    level_id = Column(Integer, ForeignKey('Level.level_id', ondelete='cascade'), primary_key=True, nullable=False)


class Statistics(Base):
    """
    The game statistics for each level played.
    """

    # region CONSTANTS

    __tablename__ = 'Statistics'
    statistics_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    points = Column(Integer, nullable=False, default=0)
    level_id = Column(Integer, ForeignKey('Level.level_id', ondelete='cascade'), nullable=False, unique=True)

    # endregion


class Level(Base):
    """
    A level that contains several items and
    present their relations to the game.
    """

    __tablename__ = 'Level'
    level_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(Unicode(50), nullable=False, unique=True)
    image = Column(Unicode(250))
    time_seg = Column(Integer, nullable=False, default=60)
    points = Column(Integer, nullable=False, default=10)
    blocked = Column(Boolean, nullable=False, default=True)
    package_id = Column(Integer, ForeignKey('Package.package_id', ondelete='cascade'), nullable=False)

    # the max distance of the relationships allowed ( if greater is more complex )
    difficulty = Column(Integer, nullable=False, default=0)

    items = orm.relation(Item, secondary='item_level',  backref='levels')
    statistic = orm.relation(Statistics, backref='levels')

    relations = None

    def are_connected(self, item1, item2):
        if self.relations is None:

            self.relations = dict([(i, i.all_related_items(self.difficulty)) for i in self.items])

        if isinstance(item1, int) and isinstance(item2, int):
            item1, item2 = self.items[item1], self.items[item2]

        return item2 in self.relations[item1] or item1 in self.relations[item2]


class Package(Base):
    """
    A package that contains several levels
    """

    # region CONSTANTS

    __tablename__ = 'Package'
    package_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(Unicode(50), nullable=False, unique=True)
    levels = relationship(Level, backref='package')
    image = Column(Unicode(250))

    # endregion


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


def update_distances():

    a = DB().get_db_session()

    for item in a.query(Item).all():
        for tag in a.query(Tag).all():
            d = tag.get_distance(item)
            if d >= 0:
                relation = [t for t in item.item_tags if t.tag == tag]

                if len(relation) == 0:
                    print("create")
                else:
                    t = relation[0]

                    if t.distance != d:
                        t.distance = d
                        print(u"Tag: {0}, Item: {1}, Distance: {2}".format(item.name, tag.name,d))
