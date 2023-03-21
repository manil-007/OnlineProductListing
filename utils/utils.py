from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import *
import xlrd
from bs4 import BeautifulSoup
import csv, json
from config.config import cfg
from datetime import datetime
import pandas as pd


def get_url(search_product):
    template = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_1'
    search_product = search_product.replace(' ', '+')
    url = template.format(search_product)
    url += '&page={}'
    return url


def search_amazon(driver, search_phrase, sp_id, num_of_products, final_output):
    search_url = get_url(search_phrase)
    for page in range(1):
        driver.get(search_url.format(str(page)))
        driver.implicitly_wait(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        rank = 1
        for i in range(num_of_products):
            product = {}
            product["id"] = sp_id
    
            if results and results[i]:
                atag = results[i].h2.a 
                product_url = 'https://www.amazon.in/' + atag.get('href')
                driver.get(product_url)
                product["url"] = product_url

            driver.implicitly_wait(3)
            product_soup = BeautifulSoup(driver.page_source, 'html.parser')
            prd_title = ""
            brand = ""
            details = ""
            prd_des = ""
            price = ""
            product_details = product_soup.find("table", {"class": "a-normal a-spacing-micro"})

            try:
                prd_title = product_soup.find("span", {"id": "productTitle"}).text.strip()
                product["title"] = prd_title
            except:
                print("Product Title Not Available")
            try:
                for row in product_details.tbody.find_all("tr"):
                    columns = row.find_all("td")

                    def getValFromTable(columnName):
                        return columnName[columnName.rfind('">') + len('">'):columnName.rfind('</span')]

                    details += (getValFromTable(str(columns[0])) + "-" + getValFromTable(str(columns[1]))) + "|"

                product["details"] = details
            except:
                print(search_phrase, ": Product Details not present")
            try:
                brand = details[details.rfind("Brand-") + len("Brand-"):details.find("|")]
                product["brand"] = brand
            except:
                print("Product Brand not present")
            try:
                des = product_soup.find("div", {"id": "feature-bullets"}).find("ul")
                prd_des = ""
                for i in des.find_all("li"):
                    prd_des += i.text + " | "
                
                product["description"] = prd_des
            except:
                print("Product Description not present")
            try:
                price = product_soup.find("span", {"class": "a-price-whole"}).text
                product["price"] = price
            except:
                print("Product Price Not Available")
            
            product["rank"] = str(rank)

            final_output[search_phrase].append(product)

            rank += 1

    return final_output

# TODO: Fix the order of parameters
def create_output_file(headless=True, sss: str=None, num_of_products: int=10):
    out = {}
    sp_id = 0

    chromeOptions = Options()
    chromeOptions.headless = headless
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)

    # stripped_search_strings is empty, so read search strings from xlsx
    if sss:
        for sp in sss:
            sp_id += 1
            out[sp] = []
            search_amazon(driver, sp, sp_id, num_of_products, out)
    else:
        out["Error"] = "Please enter a search phrase!"
    return out
