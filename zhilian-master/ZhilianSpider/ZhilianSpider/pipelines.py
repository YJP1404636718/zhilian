# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class ZhilianspiderPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        # self.client.admin.authenticate(settings['MONGO_USER'], settings['MONGO_PSW'])
        self.zhilian = self.client['zhilian']
        self.zhilianData = self.zhilian['zhiliandata']
        pass

    def process_item(self, item, spider):
        self.zhilianData.insert_one(item)
        return item

    def close_spider(self, spider):
        pass
