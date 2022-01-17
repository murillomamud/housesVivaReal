
from ctypes import addressof
from ctypes.wintypes import WCHAR
from pydoc import describe
from sunau import Au_read
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


i = 1
url = 'https://www.vivareal.com.br/venda/sp/indaiatuba/apartamento_residencial/?pagina={}'
ret = requests.get(url.format(i))

soup = bs(ret.text)

qtyHouses = float(soup.find('strong', {'class':'results-summary__count'}).text.replace('.',''))
listHouse = soup.find_all('a', {'class':'property-card__content-link js-card-title'})
#print(listHouse)
#print(qtyHouses)

house = listHouse[0]

df = pd.DataFrame(
    columns=[
        'descr',
        'address',
        'area',
        'bedroom',
        'bathroom',
        'garage',
        'value',
        'condominium',
        'wlink'
    ]
)

i = 1

while qtyHouses > df.shape[0]:

    #print(f"value i:{i} \t\t quantity:{df.shape[0]}")
    ret = requests.get(url.format(i))
    soup = bs(ret.text)
    i += 1

    listHouse = soup.find_all('a', {'class':'property-card__content-link js-card-title'})

    for house in listHouse:
        try:
            descr = house.find('span', {'class':'property-card__title'}).text.strip()
        except:
            descr = None

        try:
            address = house.find('span', {'class':'property-card__address'}).text.strip()
        except:
            address = None

        try:
            area = house.find('span', {'class':'js-property-card-detail-area'}).text.strip()
        except:
            area = None

        try:
            bedroom = house.find('li', {'class':'property-card__detail-room'}).span.text.strip()
        except:
            bedroom = None

        try:
            bathroom = house.find('li', {'class':'property-card__detail-bathroom'}).span.text.strip()
        except:
            bathroom = None

        try:
            garage = house.find('li', {'class':'property-card__detail-garage'}).span.text.strip()
        except:
            garage = None

        try:
            value = house.find('div', {'class':'property-card__price'}).p.text.strip()
        except:
            value = None

        try:
            condominium = house.find('strong', {'class':'js-condo-price'}).text.strip()
        except:
            condominium = None

        try:
            wlink = 'https://www.vivareal.com.br' + house['href']
        except:
            wlink = None

        df.loc[df.shape[0]] = [
            descr,
            address,
            area,
            bedroom,
            bathroom,
            garage,
            value,
            condominium,
            wlink
        ]
        #print(i)
        #if i == 5:
           #break

df.to_csv("houses.csv",sep=';', index=False)

##print(descr)
#print(address)
#print(area)
#print(bedroom)
#print(bathroom)
#print(garage)
#print(value)
##print(condominium)
#print(wlink)

#address
#area
#bedrooms
#wc
#garage
#value
#condominium
#link


