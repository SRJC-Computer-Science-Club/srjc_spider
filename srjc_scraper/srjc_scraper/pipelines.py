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
from .object_relational_models import Sections, Times
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

        print("opening")

        try:
            self.engine, self.controller = connect(username, password, database, url)
        except ConnectionError:
            print("error connecting")

        if not self.engine.dialect.has_table(self.engine, "sections"):  # If table don't exist, Create.
            print("RE INITIALIZING TABLE CARE CARE ")
            Table("sections", self.controller,
                  Column('section_id', Integer, primary_key=True, nullable=False),
                  Column('short_name', String),
                  Column('long_name', String),
                  Column('description', String),
                  Column('units', Float),
                  Column('status', String),
                  Column('current_enrolled', Integer),
                  Column('seats_remaining', Integer),
                  Column('start_date', Integer),
                  Column('end_date', Integer),
                  Column('final_date', Integer),
                  schema=None
                  )
            Table("times", self.controller,
                  Column("id", Integer, primary_key=True, autoincrement=True),

                  Column('monday', Boolean),
                  Column('tuesday', Boolean),
                  Column('wednesday', Boolean),
                  Column('thursday', Boolean),
                  Column('friday', Boolean),
                  Column('saturday', Boolean),
                  Column('sunday', Boolean),

                  Column('start_time', Integer),
                  Column('end_time', Integer),

                  Column('campus', String),
                  Column('room', String),

                  Column('section_id', Integer, ForeignKey('sections.section_id')),
                  schema=None
                  )
            self.controller.drop_all()
            self.controller.create_all()

        self.Session = sessionmaker(bind=self.engine)


def close_spider(self, spider):
    print(str(self.counter) + " objects pipelined into database")


def process_item(self, item, spider):
    session = self.Session()
    ime = Sections(**item)
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
