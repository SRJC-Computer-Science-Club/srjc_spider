from sqlalchemy import Sequence
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()


class Class(Base):
    __tablename__ = 'classes'
    section_id = Column('section_id', Integer, primary_key=True)
    short_name = Column('short_name', String)
    long_name = Column('long_name', String)
    description = Column('description', String)

    units = Column('units', Float)
    status = Column('status', String)

    current_enrolled = Column('current_enrolled', Integer)
    seats_remaining = Column('seats_remaining', Integer)

    start_date = Column('start_date', Integer)
    end_date = Column('end_date', Integer)
    final_date = Column('final_date', Integer)

    sections = relationship("Section")


class Section(Base):
    __tablename__ = 'sections'
    id = Column(Integer, primary_key=True, autoincrement=True)

    monday = Column('monday', Boolean)
    tuesday = Column('tuesday', Boolean)
    wednesday = Column('wednesday', Boolean)
    thursday = Column('thursday', Boolean)
    friday = Column('friday', Boolean)
    saturday = Column('saturday', Boolean)
    sunday = Column('sunday', Boolean)

    start_time = Column('start_time', Integer)
    end_time = Column('end_time', Integer)

    campus = Column('campus', String)
    room = Column('room', String)

    section_id = Column("section_id", ForeignKey('classes.section_id'))

