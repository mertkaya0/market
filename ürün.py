

from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def baglanti(url):
    request = requests.get(url)
    content = request.content
    return BeautifulSoup(content, "lxml")



def istek(market, ürün):
    name = []
    price = []
    if market == "A101":
        soup = baglanti("https://www.a101.com.tr/list/?search_text={}".format(ürün))
        ürünler = soup.find_all("ul", {"class": "product-list-general"})
        for i in ürünler:
            ad = soup.find_all("h3", {"class": "name"})
            fiyat = soup.find_all("span", {"class": "current"})
            for j in ad:
                if len(name) == 10:
                    break
                ürün_adı = (((j.text).split("\n"))[1]).rstrip().lstrip()
                name.append(ürün_adı)
            for k in fiyat:
                if len(price) == 10:
                    break
                ürün_fiyatı = float(((((str((k.text).replace("   ", " "))).split(" "))[0]).replace(".","")).replace(",","."))
                price.append(ürün_fiyatı)
        return pd.DataFrame({"Market":"A101","Ürün Adı"+(" "*7):name,"Ürün Fiyatı":price})


    if market == "CarrefourSA":
        soup = baglanti("https://www.carrefoursa.com/search/?sort=bestSeller&sortingOption=bestSeller&q={}%3Arelevance#".format(ürün))
        ürünler = soup.find_all("ul", {"class": "product-listing product-grid container-fluid"})
        for i in ürünler:
            ad = soup.find_all("span", {"class": "item-name"})
            fiyat = soup.find_all("div",{"class":"product_click"})
            for j in ad:
                if len(name) == 10:
                    break
                ürün_adı = (j.text)
                name.append(ürün_adı)
            for k in fiyat:
                a = k.find_all("input", {"id": "productPricePost"})
                for j in a:
                    if len(price) == 10:
                        break
                    prices = str(j)
                    ürün_fiyatı = round(float((prices[74:81]).replace('"', "0").strip("/>")), 2)
                    price.append(ürün_fiyatı)
        return pd.DataFrame({"Market":"CarrefourSA","Ürün Adı"+(" "*7):name,"Ürün Fiyatı":price})

    if market == "Migros":
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.migros.com.tr/arama?q={}".format(ürün))
        try:
            for i in range(1, 11):
                try:
                    adı = driver.find_element_by_xpath("/html/body/sm-root/div/main/sm-product/article/sm-list/div[2]/div[4]/div[2]/div[4]/sm-list-page-item[{}]/mat-card/div[1]/a".format(i)).text
                except:
                    adı = driver.find_element_by_xpath("/html/body/sm-root/div/main/sm-product/article/sm-list/div[2]/div[4]/div[2]/div[4]/sm-list-page-item[{}]/mat-card/div[2]/a".format(i)).text
                name.append(adı)
                try:
                    fiyat = str(driver.find_element_by_xpath("/html/body/sm-root/div/main/sm-product/article/sm-list/div[2]/div[4]/div[2]/div[4]/sm-list-page-item[{}]/mat-card/div[2]/fe-product-price/div/div/span".format(i)).text)
                except:
                    try:
                        fiyat = str(driver.find_element_by_xpath("/html/body/sm-root/div/main/sm-product/article/sm-list/div[2]/div[4]/div[2]/div[4]/sm-list-page-item[{}]/mat-card/div[3]/fe-product-price/div/div[2]/span".format(i)).text)
                    except:
                        fiyat = str(driver.find_element_by_xpath(
                            "/html/body/sm-root/div/main/sm-product/article/sm-list/div[2]/div[4]/div[2]/div[4]/sm-list-page-item[{}]/mat-card/div[3]/fe-product-price/div/div/span".format(
                                i)).text)
                price.append(float((fiyat.strip(" TL")).replace(",",".")))
        except:
            pass
        driver.close()
        return pd.DataFrame({"Market": "Migros", "Ürün Adı" + (" " * 7): name, "Ürün Fiyatı": price})

    if market == "Şok":
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.sokmarket.com.tr/arama/{}".format(ürün))
        try:
            for i in range(1, 11):
                adı = str(driver.find_element_by_xpath(
                    "//*[@id='root']/section/main/div/div/ul/li[{}]/div/a/div[2]/strong".format(i)).text)
                name.append(adı)

                try:
                    fiyat = str(driver.find_element_by_xpath(
                        f"//*[@id='root']/section/main/div/div/ul/li[{i}]/div/a/div[2]/div/span[2]").text)
                except:
                    fiyat = str(driver.find_element_by_xpath(
                        f"//*[@id='root']/section/main/div/div/ul/li[{i}]/div/a/div[2]/div").text)
                price.append(float(fiyat.replace(",", ".")))
        except:
            pass
        driver.close()
        return pd.DataFrame({"Market":"Şok","Ürün Adı"+(" "*7):name,"Ürün Fiyatı":price})



