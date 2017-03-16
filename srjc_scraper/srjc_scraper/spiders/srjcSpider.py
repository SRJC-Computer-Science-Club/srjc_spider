from __future__ import absolute_import
import scrapy
from scrapy import FormRequest, Request
from bs4 import BeautifulSoup
import re

from ..items import SrjcScraperItem
from ..functions import get_field_name, convert_item


class SRJCSpider(scrapy.Spider):
    name = "SRJC"
    url_prefix_for_classes = "https://portal.santarosa.edu/SRWeb/"

    def start_requests(self):
        urls = [
            'https://portal.santarosa.edu/SRWeb/SR_ScheduleOfClassesMobile.aspx',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        for option in soup.find_all('option'):
            if option.get_text() == "Summer 2017":
                yield FormRequest.from_response(
                    response,
                    formdata={
                        "ddlTerm": option.get('value')
                    },
                    callback=self.open_category,
                )

    def open_category(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        for item in soup.findAll("a", class_='NormalSiteLink'):
            yield Request(

                self.url_prefix_for_classes + item.get('href'),
                callback=self.open_class)

    def open_class(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        for link in soup.find_all("a", class_="NormalSiteLink"):
            if link.has_attr("title") & link.has_attr("href"):
                yield Request(
                    self.url_prefix_for_classes + link.get('href'),
                    # "https://portal.santarosa.edu/SRWeb/SR_ScheduleOfClasses.aspx?Mode=text&TermID=20175&CourseDiscipline=BIO&Course=37413",
                    callback=self.get_class_body_extract)

    def get_class_body_extract(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        all_headers = soup.find_all("tr", class_="Normal")

        names = []
        description = ""
        for child in all_headers:
            ime = child.find("td")
            # this is the workaround for how srjc structures it
            if ime is not None:
                if ime.get('title') == ime.get_text():
                    names.append(ime.get_text())

            description_container = child.find("td", title="Catalog Description")
            if description_container is not None:
                description = child.find("span", class_="Normal").get_text()

        # the way the srjc structures their headers are wonky, which is why we do it like this
        # to find the short and long name
        short_name = names[0]
        long_name = names[1]

        #   now we have long_name, short_name, and description
        #  and put it in the dictionary to convert


        for data_row in soup.find_all("tr", class_="DataRow"):
            # we do it like this to keep structure of lines, otherwise returns unordered soup
            counter = 0
            container = {'short_name': short_name,
                         'long_name': long_name,
                         'description': description}
            for data_cell in data_row.find_all("td", class_="DataCell"):
                inner_text = data_cell.find_all(text=True)
                if get_field_name(counter) is not None:
                    container[get_field_name(counter)] = inner_text
                counter += 1
            # we now have all the fields, and this is a helper method un functions that converts
            # the raw data dict to the proper yield class
            item = convert_item(container)
            if item is not None:
                yield item
            else:
                print("did not yield item")
