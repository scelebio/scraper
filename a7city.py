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

citytoday= date1.strftime('%m/%d/%Y')
citytmw =(date1 + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
cityaftertmw= (date1 + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
citynextweek= (date1 + datetime.timedelta(days=7)).strftime('%m/%d/%Y')
cityafternextweek= date8= (date1 + datetime.timedelta(days=8)).strftime('%m/%d/%Y')

from datetime import datetime
noon = datetime.strptime('12:00','%H:%M').strftime('%l:%M:%S')

driver = webdriver.Chrome('/Users/sarpercelebioglu/downloads/chromedriver')  # Optional argument, if not specified will search path.
driver.maximize_window()



driver.get('http://www.cityrentacar.com/')
driver.implicitly_wait(10)
time.sleep(2) # Let the user actually see something!


select = Select(driver.find_element_by_xpath('//*[@id="sel"]'))
select.select_by_visible_text('12:00 PM')
#select.select_by_value('261').click()
time.sleep(1)

select2 = Select(driver.find_element_by_xpath('//*[@id="sel2"]'))
select2.select_by_visible_text('12:00 PM')

driver.implicitly_wait(2)
driver.maximize_window()
#Selecting location, pickup and dropoff times


#pick up date
if time1 > noon:
    city_search_box = driver.find_element_by_id('date1').clear()
    city_search_box = driver.find_element_by_id('date1').click()
    actions = ActionChains(driver)
    actions.send_keys(citytmw)
    actions.perform()
else:
    city_search_box = driver.find_element_by_id('date1').clear()
    city_search_box = driver.find_element_by_id('date1').click()
    actions = ActionChains(driver)
    actions.send_keys(citytoday)
    actions.perform()

#drop off date
if time1 > noon:
    city_search_box = driver.find_element_by_id('date2').clear()
    city_search_box = driver.find_element_by_id('date2').click()
    actions = ActionChains(driver)
    actions.send_keys(cityaftertmw)
    actions.perform()

else:
    city_search_box = driver.find_element_by_id('date2').clear()
    city_search_box = driver.find_element_by_id('date2').click()
    actions = ActionChains(driver)
    actions.send_keys(citytmw)
    actions.perform()


city_btn = driver.find_elements_by_xpath('//*[@id="btnNext"]')
city_btn[0].click()

time.sleep(10)


#So far, we navigated through the web site. now we are going to scrape the data.

city_vehicletypes = driver.find_elements_by_xpath('//*[@class="col-md-4 col-sm-4 col-xs-6"]/div/h3')


city_rates= driver.find_elements_by_xpath('//*[@class="btn_div"]/h2[1]')

#defining the arrays for the daily rates and vehicle types
city_myvehicle=[]
city_myrate=[]

for vehicle in city_vehicletypes:
    city_myvehicle.append(vehicle.text)
    print(city_myvehicle)

for rate in city_rates:
    city_myrate.append(rate.text)
    print(city_myrate)


city_finallist=zip(city_myvehicle,city_myrate)


#extracting daily rates to the spreadsheet

wb=Workbook()
sh1=wb.active
wb['Sheet'].title='City Daily Rates'
sh1.append(['City Car type','City Daily Rates'])
sheetname ="City Weekly Rates"

#defining the second worksheet for the weekly rates
sh2= wb.create_sheet(index = 1 , title = sheetname)

for x in list(city_finallist):
    sh1.append(x)



city_pickupbtn = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/ul/li[1]/a')
city_pickupbtn.click()

if time1 > noon:
    city_search_box = driver.find_element_by_id('date2').clear()
    city_search_box = driver.find_element_by_id('date2').click()
    actions = ActionChains(driver)
    actions.send_keys(cityafternextweek)
    actions.perform()

else:
    city_search_box = driver.find_element_by_id('date2').clear()
    city_search_box = driver.find_element_by_id('date2').click()
    actions = ActionChains(driver)
    actions.send_keys(citynextweek)
    actions.perform()

city_btn = driver.find_elements_by_xpath('//*[@id="btnNext"]')
city_btn[0].click()



city_vehicletypes7 = driver.find_elements_by_xpath('//*[@class="col-md-4 col-sm-4 col-xs-6"]/div/h3')


city_rates7= driver.find_elements_by_xpath('//*[@class="btn_div"]/h2[1]')

#defining the arrays for the daily rates and vehicle types
city_myvehicle7=[]
city_myrate7=[]

for vehicle7 in city_vehicletypes7:
    city_myvehicle7.append(vehicle7.text)
    print(city_myvehicle7)

for rate7 in city_rates7:
    city_myrate7.append(rate7.text)
    print(city_myrate7)


city_finallist7=zip(city_myvehicle7,city_myrate7)

sh2.append(['Car type','Weekly Rates'])


for x in list(city_finallist7):
    sh2.append(x)



wb.save("finaldatacity.xlsx")