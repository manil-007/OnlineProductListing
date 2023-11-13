import xlrd
import openai
import logging

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from tenacity import retry, stop_after_attempt, wait_random_exponential

# Project imports
from config.config import cfg
from utils.ProvisionOpenAI import ProvisionOpenAI

ProvisionOpenAI.set_api_key(cfg["openapi"]["secret"])
openai.api_key = ProvisionOpenAI.get_api_key()
logger = logging.getLogger(__name__)


def get_url(search_product):
    template = 'https://www.amazon.in/s?k={}'
    search_product = search_product.replace(' ', '+')
    url = template.format(search_product)
    url += '&page={}'
    return url


def search_amazon(driver, search_phrase, sp_id, num_of_products, final_output):
    logger.info("Searching for product : {a}".format(a=search_phrase))
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

            driver.implicitly_wait(5)
            product_soup = BeautifulSoup(driver.page_source, 'html.parser')
            details = ""
            product_details = product_soup.find("table", {"class": "a-normal a-spacing-micro"})

            try:
                prd_title = product_soup.find("span", {"id": "productTitle"}).text.strip()
                product["title"] = prd_title
            except:
                logger.error("{a} : Product Title Not Available".format(a=search_phrase))
                product["title"] = ""
            try:
                for row in product_details.tbody.find_all("tr"):
                    columns = row.find_all("td")

                    def getValFromTable(columnName):
                        return columnName[columnName.rfind('">') + len('">'):columnName.rfind('</span')]

                    details += (getValFromTable(str(columns[0])) + "-" + getValFromTable(str(columns[1]))) + "|"

                product["details"] = details
            except:
                logger.error("{a} : Product Details Not Available".format(a=search_phrase))
                product["details"] = ""
            try:
                brand = details[details.rfind("Brand-") + len("Brand-"):details.find("|")]
                product["brand"] = brand
            except:
                logger.error("{a} : Product Brand Not Available".format(a=search_phrase))
                product["brand"] = ""
            try:
                des = product_soup.find("div", {"id": "feature-bullets"}).find("ul")
                prd_des = ""
                for i in des.find_all("li"):
                    prd_des += i.text + " | "
                
                product["description"] = prd_des
            except:
                logger.error("{a} : Product Description Not Available".format(a=search_phrase))
                product["description"] = ""
            try:
                price = product_soup.find("span", {"class": "a-price-whole"}).text
                product["price"] = price
            except:
                logger.error("{a} : Product Price Not Available".format(a=search_phrase))
                product["price"] = ""
            
            product["rank"] = str(rank)

            final_output[search_phrase].append(product)

            rank += 1

    return final_output

def create_output_file(headless, input_file_name: str=None, sss: str=None, num_of_products: int=10):
    out = {}
    sp_id = 0

    browser_options = Options()
    browser_options.add_argument("-headless") if headless else None

    driver = webdriver.Firefox(options=browser_options)
    driver.delete_all_cookies()

    # stripped_search_strings is empty, so read search strings from xlsx
    if sss:
        for sp in sss:
            sp_id += 1
            out[sp] = []
            search_amazon(driver, sp, sp_id, num_of_products, out)
    else:
        wb = xlrd.open_workbook(input_file_name)
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)

        for i in range(1, sheet.nrows):
            sp = str(sheet.cell_value(i, 1))
            sp_id = +1
            out[sp] = []
            search_amazon(driver, sp, sp_id, num_of_products, out)
    return out


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(60))
def completion_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)


def trimList(keywords):
    list_of_keywords = [sub.replace("\n", "") for sub in keywords]
    list_of_keywords = [sub.strip() for sub in list_of_keywords]
    return list_of_keywords


def trimText(data):
    trimData = data.replace("\n", "").replace('"', '')
    trimData = trimData.strip()
    return trimData
