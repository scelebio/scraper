import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import timedelta
from selenium.webdriver.support.ui import Select


#time1 = (time.strftime("%I:%M %p")) # output format PM AM format
time1 = (time.strftime('%H:%M:%S')) # 24 hours format timestamp

#defining today's date
date1 = datetime.date.today()
date2 = date1.strftime("%b%e") #output format
today= date2[-2:].replace(' 0','')# getting the last 2 characters of the date. this data will be used to click on the calendar.

#defining tmw's date
date4= (date1 + datetime.timedelta(days=1)).strftime("%b%e")
tmw= date4[-2:].replace(' 0','')

#defining the day after tmw
date5= (date1 + datetime.timedelta(days=2)).strftime("%b%e")
tmw2 = date5[-2:].replace(' 0','')


from datetime import datetime
noon = datetime.strptime('12:00','%H:%M').strftime('%l:%M:%S')
driver = webdriver.Chrome('/Users/sarpercelebioglu/downloads/chromedriver')  # Optional argument, if not specified will search path.
driver.maximize_window()



driver.get('http://www.hertz.com/')
driver.implicitly_wait(10)
time.sleep(2) # Let the user actually see something!

#Selecting location, pickup and dropoff date/times
trigger = driver.find_elements_by_id('resformStartTrigger')
trigger[0].click() #activate the location tab
pickup_location = driver.find_elements_by_id('pickup-location')
pickup_location[0].send_keys('sfoc10')
pickup_time = Select(driver.find_element_by_id('pickupTimeSelect'))
pickup_time.select_by_visible_text('12:00 Noon')
pickup_time = Select(driver.find_element_by_id('dropoffTimeSelect'))
pickup_time.select_by_visible_text('12:00 Noon')
time.sleep(0.5)


#Selecting pick up date
pickup_date =driver.find_element_by_xpath('//*[@id="pickup-date-box"]/div[1]').click()
alldates=driver.find_elements_by_xpath('/html/body/div[2]/div[1]/div/table/tbody/tr/td')
for dateelement in alldates:
    date=dateelement.text
    print(date)
    if time1 > noon:
        if date==tmw:
            dateelement.click()
            break
    else:
        if date==today:
            dateelement.click()
            break

#Selecting drop off date
pickup_date =driver.find_element_by_xpath('//*[@id="dropoff-date-box"]/div[1]').click()
alldates=driver.find_elements_by_xpath('/html/body/div[2]/div[1]/div/table/tbody/tr/td')
for dateelement in alldates:
    date=dateelement.text
    print(date)
    if time1 > noon:
        if date==tmw2:
            dateelement.click()
            break
    else:
        if date==today:
            dateelement.click()
            break

time.sleep(2) # let the user see the inputs are correct.

#Clicking on 'book the reservation' button
btn = driver.find_elements_by_xpath('//*[@id="res-submit-btns"]/div/div/div[2]/button')
btn[0].click()
