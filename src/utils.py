from selenium import webdriver
from webdriver_manager.chrome import *
import xlrd
from bs4 import BeautifulSoup
import csv
from config import config
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
        for i in range(config.numberOfProducts):
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


def createOutputFile(inputFileName, outputFileName):
    loc = inputFileName
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    out = []
    driver = webdriver.Chrome(ChromeDriverManager().install())
    for i in range(1, sheet.nrows):
        print("Extracting for -> ", str(sheet.cell_value(i, 1)))
        out += search_amazon(driver, str(sheet.cell_value(i, 1)))
    driver.quit()
    now = datetime.now()
    curr_datetime = now.strftime("%d-%m-%Y_%H-%M-%S")

    fileName = "output/" + outputFileName + "_" + curr_datetime + ".csv"
    f = open(fileName, 'w')
    fields = ["Parent Product", "Rank", "Url", "Title", "Details", "Brand", "Price", "Description"]
    writer = csv.writer(f)
    writer.writerow(fields)
    writer.writerows(out)

    f.close()
