import time
import datetime
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import timedelta
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

#time1 = (time.strftime("%I:%M %p")) # output format PM AM format
time1 = (time.strftime('%H:%M:%S')) # 24 hours format timestamp

#defining today's date
date1 = datetime.date.today()
date2 = date1.strftime("%b%e") #output format
today= date2[-2:].replace(' 0','').replace(' ','')# getting the last 2 characters of the date. this data will be used to click on the calendar.
todaymonth=date2[0:3]

#defining tmw's date
date4= (date1 + datetime.timedelta(days=1)).strftime("%b%e")
tmw= date4[-2:].replace(' 0','').replace(' ','')
tmwmonth=date4[0:3]

#defining the day after tmw
date5= (date1 + datetime.timedelta(days=2)).strftime("%b%e")

tmw2 = date5[-2:].replace(' 0','').replace(' ','')


#selecting the next week's dates. 7 days or 7+1.
#7 days:
date7= (date1 + datetime.timedelta(days=7)).strftime("%b%e")
nextweek7= date7[-2:].replace(' 0','').replace(' ','')
nextweek7month= date7[0:3]
#7 days+1 :
date8= (date1 + datetime.timedelta(days=8)).strftime("%b%e")
nextweek8= date8[-2:].replace(' 0','').replace(' ','')
nextweek8month=date8[0:3]

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
#time.sleep(5)
#search_box[0].send_keys(Keys.ENTER)
time.sleep(1)
pickuptime_arrow= driver.find_element_by_xpath('//*[@id="pickupTime"]/div').click()
time.sleep(3)
pickuptime=driver.find_element_by_xpath("//*[text()='12:00 PM']")
driver.execute_script("arguments[0].click();", pickuptime)

cookies=driver.find_elements_by_id("acceptAndCloseButton")
cookies[0].click()

'''
print("today " + today)
print("date2 " + date2)
print("tmw "+tmw)
print("date4 "+date4)
print("date5 "+date5)
print("tmw2 " +tmw2)
print("nextweek7 "+nextweek7)
print("date7 "+date7)
print("nextweek8 " +nextweek8)
print("date8 " +date8)
print(todaymonth)
print(tmwmonth)
print(nextweek7month)
print(nextweek8month)
'''
#Selecting pick up date
pickup_date =driver.find_element_by_xpath('//*[@id="pickupDate"]').click()

#alldates=driver.find_elements_by_xpath('/html/body/div[1]/div[1]/main/div[2]/div/div/div[3]/div[1]/div[1]/div[2]/div[3]/div/div')
alldates=driver.find_elements_by_xpath('/html/body/div[1]/div[1]/main/div[1]/div/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/div/div')
                                        
driver.maximize_window()

for dateelement in alldates:
    date=dateelement.text

  
    if time1 > noon:
        if date==tmw:
            dateelement.click()
            break
    else:
        if date==today:
            dateelement.click()
            break

#Selecting drop off date
pickup_date =driver.find_element_by_xpath('//*[@id="dropoffDate"]').click()
#alldates=driver.find_elements_by_xpath('/html/body/div[1]/div[1]/main/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[3]/div/div')
alldates=driver.find_elements_by_xpath('/html/body/div[1]/div[1]/main/div[1]/div/div/div/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/div/div')
driver.maximize_window()
for dateelement in alldates:
    date=dateelement.text
    #print(date)
    if time1 > noon:
        if date==tmw2:
            dateelement.click()
            break
    else:
        if date==tmw:       #this was "today". I noticed that I forgot to change it as "tmw". 
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

#defining the arrays for the daily rates and vehicle types
myvehicle=[]
myrate=[]

for vehicle in vehicletypes:
    myvehicle.append(vehicle.text)

for rate in rates:
    myrate.append(rate.text)


finallist=zip(myvehicle,myrate)

#extracting daily rates to the spreadsheet

wb=Workbook()
sh1=wb.active
wb['Sheet'].title='Hertz Daily Rates'
sh1.append(['Car type','Daily Rates'])
sheetname ="Hertz Weekly Rates"

#defining the second worksheet for the weekly rates
sh2= wb.create_sheet(index = 1 , title = sheetname)

for x in list(finallist):
    sh1.append(x)

#we got the daily rates successfuly, Now we are going to scrape the weekly rates
#Clicking on 'modify reservation' button
modifybtn = driver.find_elements_by_xpath('//*[@id="locationsEdit"]')
modifybtn[0].click()
#Selecting drop off date (next week)

pickup_date =driver.find_element_by_xpath('//*[@id="dropoffDate"]').click()
time.sleep(3)
alldates2=driver.find_elements_by_xpath('/html/body/div[1]/div[1]/main/div[1]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[3]/div/div')

#when the next week is in the next month, we need to navigate to the next month.

driver.maximize_window()
for dateelement2 in alldates2:
    date_2=dateelement2.text
    if time1 > noon:
        if tmwmonth==nextweek8month:
            if date_2==nextweek8:
                dateelement2.click()
                break
        else:
            actions = ActionChains(driver) 
            actions.send_keys(Keys.TAB)
            actions.send_keys(Keys.ARROW_RIGHT)
            actions.perform()
            if date_2==nextweek8:
                dateelement2.click()
                break    
    else:
        if tmwmonth==nextweek7month:
            if date_2==nextweek7:
                dateelement2.click()
        else:
            actions = ActionChains(driver) 
            actions.send_keys(Keys.TAB)
            actions.send_keys(Keys.ARROW_RIGHT)
            actions.perform()
            if date_2==nextweek7:
                dateelement2.click()      
                break

time.sleep(2) # let the user see the inputs are correct.

#after inputting the right dates, we are going to click update/edit itinary button.
updatebtn = driver.find_elements_by_xpath('//*[@id="updateEditItinaryButton"]')
updatebtn[0].click()
time.sleep(5)

#after listing the cars for a week, we are going to repeat the scraping process.
vehicletypes7 = driver.find_elements_by_class_name('VehicleCardDescription-module__vehicleCollectionName__8ED7j')
rates7= driver.find_elements_by_xpath('//*[@class="PriceAndButtonNew-module__integer__1ADKD"]')
myvehicle7=[]
myrate7=[]



for vehicle7 in vehicletypes7:
    myvehicle7.append(vehicle7.text)

for rate7 in rates7:
    myrate7.append(rate7.text)


finallist7=zip(myvehicle7,myrate7)

sh2.append(['Car type','Weekly Rates'])


for x in list(finallist7):
    sh2.append(x)

#saving the data to the spreadsheet.
wb.save("finaldata.xlsx")