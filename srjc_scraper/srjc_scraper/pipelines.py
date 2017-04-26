# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Table, Column, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import sessionmaker
from .functions import connect
from .object_relational_models import Class, Section
from os.path import join, dirname
from dotenv import get_variable

dotenv_path = join(dirname(__file__), '.env')


# to turn this on so into settings
class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def obj_dict(self, obj):
        return obj.__dict__

    def process_item(self, item, spider):
        print("should be processing item in here")
        # json_string = json.dumps(item, default=self.obj_dict)
        # self.file.write
        print(item)
        return item


# need to turn this on
class UploadToPostGres(object):
    def open_spider(self, spider):
        self.counter = 0

        password = get_variable(dotenv_path, "Password")
        username = get_variable(dotenv_path, "Username")
        url = get_variable(dotenv_path, "URL")
        database = get_variable(dotenv_path, "Database")

        try:
            self.engine, self.controller = connect(username, password, database, url)
        except ConnectionError:
            print("error connecting")

        self.Session = sessionmaker(bind=self.engine)


    def close_spider(self, spider):
        print(str(self.counter) + " objects pipelined into database")
        self.Session.close_all()


    def process_item(self, item, spider):
        session = self.Session()
        ime = Class(**item)
        try:
            session.add(ime)
            session.commit()
            self.counter += 1
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
