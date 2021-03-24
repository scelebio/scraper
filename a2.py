import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
date1 = datetime.date.today()
date1 = date1.strftime("%b %d") #output format
time1 = (time.strftime("%I:%M %p")) # output format
driver = webdriver.Chrome('/Users/sarpercelebioglu/downloads/chromedriver')  # Optional argument, if not specified will search path.
driver.get('http://www.hertz.com/')
time.sleep(2) # Let the user actually see something!
search_box = driver.find_elements_by_id('pickup-input')
search_box[0].send_keys('sfoc10')
time.sleep(1)
#pick_up = driver.find_elements_by_value("date1")
search_box[0].send_keys(Keys.ENTER)
time.sleep(1) # Let the user actually see something!
cont_btn = driver.find_elements_by_id('continueReservationButton')
cont_btn[0].send_keys(Keys.ENTER)
print(date1)
print(time1)
#driver.quit()