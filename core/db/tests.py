# -*- coding: utf-8 -*-
import os

from db_orm import  DB, Item, ItemLevel, Level
from core.db.ItemsGraph import ItemGraph


def folder_files(folder):
    files = []

    # walk for the folder file system tree
    for root, dirs, filenames in os.walk(folder):
        for f in filenames:
            try:
                if unicode(f).lower().endswith(u".png"):
                    files.append(unicode(os.path.join(root, f)))

            except Exception as ex:
                print("Errors in get folder files. On file " + unicode(f) + ". " + ex.message)

    return files


def load_items_from_folder():
    f = folder_files("fotos edited")
    items = []
    for item in f:
        image = os.path.basename(item)

        name = image.replace(".png","")
        full_name = name.split("_")

        name = ""
        for name_part in full_name:
            if len(name_part) > 0:
                name += name_part[0].upper() + name_part[1:] + " "

        items.append((name, image))

    # con = DB().get_db_session()
    #
    # for n, img in items:
    #     con.add(Item(name=n, image=img))
    #
    # con.commit()

con = DB().get_db_session()

g = ItemGraph(con.query(Item).all())

# l = g.randomized(0.8)
#
# print(len(l))
#
# for i in l:
#
#     level = Level(name="", image="", package_id=0)
#     con.add(level)
#
#     print(u"Level:")
#     for item in i:
#         print(u"----> {0} {1}".format(item[0], item[1]))
#
#         it_level = ItemLevel()
#         it_level.item1 = item[0]
#         it_level.item2 = item[1]
#         it_level.level = level
#
#         con.add(it_level)
#
# con.commit()

