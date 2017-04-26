import re
import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from .object_relational_models import Section
from .items import SrjcScraperItem
import datetime as dt


def convert_item(dict):
    # try:
    srjc_item = SrjcScraperItem()
    # this means that the sections id didnt exist, so its a work experience class
    try:
        srjc_item['section_id'] = int(dict['section_id'][0])
    except ValueError:
        print("error with section_id")
        return None

    srjc_item['short_name'] = dict['short_name']
    srjc_item['long_name'] = dict['long_name']
    srjc_item['description'] = dict['description']

    srjc_item['units'] = float(dict['units'][0])
    srjc_item['status'] = dict['status'][0]

    srjc_item['current_enrolled'] = int(dict['current_enrolled'][0])
    srjc_item['seats_remaining'] = int(dict['seats_remaining'][0])

    dates_array = dict['date_start/end'][0].split("-")

    srjc_item['start_date'] = convert_date_to_int(dates_array[0])
    srjc_item['end_date'] = convert_date_to_int(dates_array[1])

    # srjc_item['final_date'] = convert_date_to_int(dict['final_exam_date'][0])
    # print(dict)
    try:

        srjc_item['sections'] = generate_times(dict['days'],
                                            dict['hours'],
                                            dict['location'],
                                            dict['room'])
    except ValueError:
        print("error in calculationing classes")
        return None
    return srjc_item

    # except AttributeError or IndexError:
    #     return None
    # except ValueError:
    #     print("a business class so no valid section id")
    #     return None


def generate_times(days, hours, campus, room):
    section_array = []
    for index, time in enumerate(days):
        split_time = split_by_weekday(time)
        new_section = Section()

        # handling weekdays
        new_section.monday = 'M' in split_time
        new_section.tuesday = 'T' in split_time
        new_section.wednesday = 'W' in split_time
        new_section.thursday = 'Th' in split_time
        new_section.friday = 'F' in split_time
        new_section.saturday = 'Sat' in split_time
        new_section.sunday = 'Sun' in split_time

        # handling room
        if len(campus) > 1:
            new_section.room = room[index]
        else:
            new_section.room = room[0]

        # handling hours
        if len(hours) > 1:
            hours_array = hours[index].split("-")
            new_section.start_time = convert_to_military_time(hours_array[0])
            new_section.end_time = convert_to_military_time(hours_array[1])
        else:
            hours_array = hours[0].split("-")
            new_section.start_time = convert_to_military_time(hours_array[0])
            new_section.end_time = convert_to_military_time(hours_array[1])

        # handling campus
        if len(campus) > 1:
            new_section.campus = campus[index]
        else:
            new_section.campus = campus[0]
        section_array.append(new_section)
    return section_array


def get_field_name(x):
    try:
        return {
            1: "section_id",
            2: "days",
            3: "hours",
            4: "instructor",
            5: "location",
            6: "room",
            7: "units",
            8: "status",
            9: "total_seats",
            10: "current_enrolled",
            11: "seats_remaining",
            12: "date_start/end",
            13: "final_exam_date",
        }[x]
    except KeyError:
        return None


def convert_to_military_time(time):
    array = time.split(":")
    hour = int(array[0])
    if "pm" in array[1]:
        hour += 12
        minute = int(array[1].replace("pm", ""))
    else:
        minute = int(array[1].replace("am", ""))
    return hour * 100 + minute


def convert_date_to_int(input_string):
    array = input_string.split("/")
    if array[0] == '\xa0':
        return None
    return (int(array[0]) * 100) + int(array[1])


def split_by_weekday(input_string):
    arrays = re.split("([MWF]{1})|([Th]{2})|([Sat|Sun]{3})|([T^h]{1})", input_string)
    unclean_array = [item for item in arrays if (item is not None) & (item != '')]
    # i know this is really hack but if you can find a one line
    # regex to do it I wold love everyone

    flag = False
    for item in unclean_array:
        if item == "TT":
            unclean_array.remove(item)
            flag = True
    if flag:
        unclean_array.append("T")
        unclean_array.append("Th")

    return [item for item in unclean_array if item != 'h']


def connect(user, password, db, host, port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    engine = create_engine(url, echo=True)

    # We then bind the connection to MetaData()
    metadata = MetaData(bind=engine)

    return engine, metadata
