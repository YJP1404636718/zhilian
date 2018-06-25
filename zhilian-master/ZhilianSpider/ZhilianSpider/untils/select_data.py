# -*- coding: utf-8 -*-
import pymongo


def parse():
    client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    # client.admin.authenticate("", "")
    db = client.area
    city_name = db.Zhilian_area
    data = city_name.find()
    return data
#
# for i in parse():
#     print(i['area'])
