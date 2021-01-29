from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen ('http://pythonscraping.com/pages/warandpeace.html')
bs= BeautifulSoup(html.read(),'html.parser')
nameList = bs.find_all('span',{'class':'green'})
for name in nameList:
    print(name.get_text())
print('simdi kirmizilar')
nameList2 = bs.find_all('span',{'class':'red'})
for name in nameList2:
    print(name.get_text())