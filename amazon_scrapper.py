from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import *
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
import requests
import json
import time
import xlrd
from bs4 import BeautifulSoup
import csv

def get_url(search_product):
    template = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_1'
    search_product = search_product.replace(' ', '+')
    url = template.format(search_product)
    url += '&page={}'
    return url

def search_amazon(prd_name):
  #driver = webdriver.Chrome(ChromeDriverManager().install())
  final_output = []
  search_url = get_url(prd_name)
  for page in range(1):
    driver.get(search_url.format(str(page)))
    driver.implicitly_wait(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    rank = 1
    # Currently extracting top 5 products from the amazon and soon it be taken from config
    # Change this value to 'n', for extracting top 'n' products
    for i in range(5):
        item = results[i]
        atag = item.h2.a
        product_url = 'https://www.amazon.in/' + atag.get('href')
        driver.get(product_url)
        driver.implicitly_wait(3)
        product_soup = BeautifulSoup(driver.page_source, 'html.parser')
        prd_title = ""
        try:
          prd_title = product_soup.find("span", {"id": "productTitle"}).text.strip()
        except:
          print("Product Title Not Available")
        prd_des = ""
        try:
          des = product_soup.find("div", {"id": "feature-bullets"}).find("ul")
          prd_des = ""
          for i in des.find_all("li"):
            prd_des += i.text + " | "
        except:
          print("Product Description not present")
        price = ""
        try:
          price = product_soup.find("span", {"class": "a-price-whole"}).text
        except:
          print("Product Price Not Available")
        final_output.append([prd_name, str(rank), product_url, prd_title, price, prd_des])
        print([prd_name, str(rank), product_url, prd_title, price, prd_des])
        rank += 1
  #driver.quit()
  print("---DONE---")
  return final_output

# The file name will be taken from config
loc = ('test.xlsx')
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
out = []
driver = webdriver.Chrome(ChromeDriverManager().install())
for i in range(1, sheet.nrows):
  print("Extacting for -> ", str(sheet.cell_value(i, 1)))
  out += search_amazon(str(sheet.cell_value(i, 1)))
driver.quit()

fileName = 'extractedData.csv'
f = open(fileName, 'w')
fields = ["Parent Product", "Rank", "Url", "Title", "Price", "Description"] 
writer = csv.writer(f)
writer.writerow(fields)
writer.writerows(out)

f.close()
