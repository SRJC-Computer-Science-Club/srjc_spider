srjc_spider
  This is the scraper for the srjc scheduler
==========================================
#In order to run:

## Authentication
  You must either get the proper credientials from be or josh Alan to connect to the live databse

 else inside of pipeline and the connect function, you must declare your own db and credentials

### Libraries
  Uses a combination of (scrapy)[https://scrapy.org/] and (Beautiful soup)[https://www.crummy.com/software/BeautifulSoup/bs4/doc/]
  A beta using (selenium)[http://www.seleniumhq.org/] has been provided inside of srjc_selenium

This shows how to properly yield and use the twisted-scrapy framework, more to come involving middleware
specficially for other colleges support and hopefuly a net to just scrape all at once for multiple colleges

### TODOS 
  1. Syntax simplification
  2. Support for classes that do not meet at a set time
  3. Support for classes that do not have sections names

In progress: Current version is 0.1.0
