import time
import datetime
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import timedelta
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


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

#Selecting location, pickup and dropoff times
search_box = driver.find_elements_by_id('pickup-input')
search_box[0].send_keys('sfoc10')
time.sleep(1)
search_box[0].send_keys(Keys.ENTER)
time.sleep(1)
pickuptime_arrow= driver.find_element_by_xpath('//*[@id="pickupTime"]/div').click()
time.sleep(10)
pickuptime=driver.find_element_by_xpath("//*[text()='12:00 PM']")
driver.execute_script("arguments[0].click();", pickuptime)

cookies=driver.find_elements_by_id("acceptAndCloseButton")
cookies[0].click()

print(today)
print(tmw)
print(noon)
print(time1)
print(len(tmw))


#Selecting pick up date
pickup_date =driver.find_element_by_xpath('//*[@id="pickupDate"]').click()

alldates=driver.find_elements_by_xpath('/html/body/div[1]/div[1]/main/div[2]/div/div/div[3]/div[1]/div[1]/div[2]/div[3]/div/div')
driver.maximize_window()

for dateelement in alldates:
    date=dateelement.text
    #print(date)
    #print(date1)
    #print(len(date))
    #print(len(date1))
    if time1 > noon:
        if date==tmw:
            #driver.execute_script("arguments[0].scrollIntoView();", dateelement)
            #time.sleep(1)
            dateelement.click()
            #driver.execute_script("arguments[0].click();", dateelement)
            break
    else:
        if date==today:
            dateelement.click()
            break

#Selecting drop off date
pickup_date =driver.find_element_by_xpath('//*[@id="dropoffDate"]').click()
alldates=driver.find_elements_by_xpath('/html/body/div[1]/div[1]/main/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[3]/div/div')
driver.maximize_window()
for dateelement in alldates:
    date=dateelement.text
    #print(date)
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
btn = driver.find_elements_by_xpath('//*[@id="continueReservationButton"]')
btn[0].click()

time.sleep(10)

#So far, we navigated through the web site. now we are going to scrape the data.

vehicletypes = driver.find_elements_by_class_name('VehicleCardDescription-module__vehicleCollectionName__8ED7j')

rates= driver.find_elements_by_xpath('//*[@class="PriceAndButtonNew-module__integer__1ADKD"]')


myvehicle=[]
myrate=[]

for vehicle in vehicletypes:
    myvehicle.append(vehicle.text)

for rate in rates:
    myrate.append(rate.text)


finallist=zip(myvehicle,myrate)

#fields= ['Car Type','Rate','period']


wb=Workbook()
sh1=wb.active
wb['Sheet'].title='Hertz Daily Rates'
sh1.append(['Car type','Rate'])


for x in list(finallist):
    sh1.append(x)

wb.save("finaldata.xlsx")
