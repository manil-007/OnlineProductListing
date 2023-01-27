from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import *
import xlrd
from bs4 import BeautifulSoup
import csv
from config.config import cfg
from datetime import datetime
import re


def get_url(search_product):
    template = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_1'
    search_product = search_product.replace(' ', '+')
    url = template.format(search_product)
    url += '&page={}'
    return url


def search_amazon(driver, prd_name):
    final_output = []
    search_url = get_url(prd_name)
    for page in range(1):
        driver.get(search_url.format(str(page)))
        driver.implicitly_wait(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        rank = 1
        for i in range(cfg["app"]["number_of_products"]):
            item = results[i]
            atag = item.h2.a
            product_url = 'https://www.amazon.in/' + atag.get('href')
            driver.get(product_url)
            driver.implicitly_wait(3)
            product_soup = BeautifulSoup(driver.page_source, 'html.parser')
            prd_title = ""
            product_details = product_soup.find("table", {"class": "a-normal a-spacing-micro"})

            try:
                prd_title = product_soup.find("span", {"id": "productTitle"}).text.strip()
            except:
                print("Product Title Not Available")
            details = ""
            try:
                for row in product_details.tbody.find_all("tr"):
                    columns = row.find_all("td")

                    def getValFromTable(columnName):
                        return columnName[columnName.rfind('">') + len('">'):columnName.rfind('</span')]

                    details += (getValFromTable(str(columns[0])) + "-" + getValFromTable(str(columns[1]))) + "|"

            except:
                print("Product Details not present")
            brand = ""
            try:
                brand = details[details.rfind("Brand-") + len("Brand-"):details.find("|")]
            except:
                print("Product Brand not present")
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
            final_output.append([prd_name, str(rank), product_url, prd_title, details, brand, price, prd_des])
            print([prd_name, str(rank), product_url, prd_title, details, brand, price, prd_des])
            rank += 1
    # driver.quit()
    print("---DONE---")
    return final_output


def create_output_file(input_file_name, output_file_name, headless):
    loc = input_file_name
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    out = []

    chromeOptions = Options()
    chromeOptions.headless = headless
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)

    for i in range(1, sheet.nrows):
        print("Extracting for -> ", str(sheet.cell_value(i, 1)))
        out += search_amazon(driver, str(sheet.cell_value(i, 1)))
    
    driver.quit()
    
    now = datetime.now()
    curr_datetime = now.strftime("%d-%m-%Y_%H-%M-%S")

    fileName = "output/" + output_file_name + "_" + curr_datetime + ".csv"
    f = open(fileName, 'w')
    fields = ["Parent Product", "Rank", "Url", "Title", "Details", "Brand", "Price", "Description"]
    writer = csv.writer(f)
    writer.writerow(fields)
    writer.writerows(out)

    f.close()
