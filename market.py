

import googlemaps
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def your_loc():
    options = Options()
    options.headless = False
    options.add_argument("--window-size=0,0")
    driver = webdriver.Chrome(options=options)
    url = "https://findmylocation.org/"
    driver.set_window_position(2000,2000)
    driver.get(url)

    my_lat = float(driver.find_element_by_xpath("//*[@id='latitude']").text)
    my_lng = float(driver.find_element_by_xpath("//*[@id='longitude']").text)

    driver.close()

    return (my_lat,my_lng)


def market(your_location):
    market_adi = ["Migros","CarrefourSA","Şok","A-101"]
    map_client = googlemaps.Client("**YOUR_API_KEY**")
    location = your_location
    distance = 350
    business_list = []
    for i in market_adi:
        response = map_client.places_nearby(location=location, name=i, radius=distance)
        business_list.extend(response.get("results"))

        def konum_isim(liste):
            lat = []
            lng = []
            m_adı = []
            for i in liste:
                lat.append(((i["geometry"])["location"])["lat"])
                lng.append(((i["geometry"])["location"])["lng"])
                m_adı.append((i["name"]))
            dataframe = pd.DataFrame({"Lat": lat,"Lng":lng, "Market": m_adı})
            return dataframe

    return konum_isim(business_list)







