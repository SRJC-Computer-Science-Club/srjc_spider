import time
from selenium import webdriver

# FIRST RUN WITH SELENIUM

driver = webdriver.Chrome("/Users/drunkengranite/Downloads/chromedriver")
driver.implicitly_wait(30)
driver.get('https://portal.santarosa.edu/SRWeb/SR_ScheduleOfClasses.aspx')

class_options = driver.find_elements_by_xpath("//option")
print("starting the trawler");
test = class_options[1]
test.click()

top_levels = driver.find_elements_by_xpath("//a[starts-with(@id, 'TreeView1n')]")
print("opening the top level elements")
for element in top_levels:
    element.click()
    time.sleep(.5)

print("getting the second shit for this thing")
test = 0
for element in driver.find_elements_by_xpath("//a[starts-with(@id, 'TreeView1t')]"):
    if len(element.text) > 2:
        element.click()
        time.sleep(1)
# we do it like this because aspx disconnects the element from the DOM window. try and fix it
# failure count: 2

print("saving elements cuz .NET is stupid")
name_list = []
for element in driver.find_elements_by_xpath("//a[@title]"):
    name_list.append(element.get_attribute("title"))

for name in name_list:
    # yeah i know its hacky deal with it
    print(name)
    element = driver.find_element_by_xpath('//a[@title="%s"]' % name)
    if element is not None:
        element.click()
        print("found this shit")
        time.sleep(1.3)


        #this is where we get the popped off method
    else:
        print("couldnt find this shiz")


print("closing")
driver.close()
