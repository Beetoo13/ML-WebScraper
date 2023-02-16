import os, time, random
import xlsxwriter
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from helperFunctions import *

# Load dot environment
load_dotenv()

# Setup for Selenium browser
driver_path = os.getenv("DRIVER_PATH")
binary_path = os.getenv("BINARY_PATH")
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"
firefox_service = Service(driver_path)
firefox_options = Options()
firefox_options.set_preference('general.useragent.override', user_agent)

# Creating workbook for the excel file
workbook = xlsxwriter.Workbook("ProductsList.xlsx")

# Adding format to cells
title_cell_format = workbook.add_format({
    'bold': True,
})
number_cell_format = workbook.add_format({
    'bold': True,
    'num_format': '$#,##0.00'
})

percentage_cell_format = workbook.add_format({
    'bold': True,
    'num_format': '0.00%'
})

# Calling initial cells
products_workbook = workbook.add_worksheet(name="Products-list")
products_workbook.write("A1", "Product title")
products_workbook.write("B1", "Discounted price")
products_workbook.write("C1", "Original price")
products_workbook.write("D1", "Discount")
products_workbook.write("E1", "Product URL")

# Setting formats for columns
products_workbook.set_column('A:A', None, title_cell_format)
products_workbook.set_column('B:B', None, number_cell_format)
products_workbook.set_column('C:C', None, number_cell_format)
products_workbook.set_column('D:D', None, percentage_cell_format)

# Base url
base_url = "https://www.mercadolibre.com.mx/ofertas?container_id=MLM779363-4&page="
# Number of pages of the offers url
pages = 20
# Excel index counter
idx = 2

# Launch firefox
browser = webdriver.Firefox(service=firefox_service, options=firefox_options)

for page in range(1, pages + 1):
    browser.get(f"{base_url}{page}")

    products = browser.find_elements(By.CLASS_NAME, "promotion-item")

    for product in products:
        product_title = getProductTitle(product)
        original_price = getOriginalPrice(product)
        discounted_price = getDiscountedPrice(product)
        discount = getDiscount(product)
        product_url = getProductUrl(product)

        if (validateProduct(product_title, original_price, discounted_price,
                            discount, product_url)):
            products_workbook.write(f"A{idx}", product_title)
            products_workbook.write(f"B{idx}", int(original_price))
            products_workbook.write(f"C{idx}", int(discounted_price))
            products_workbook.write(f"D{idx}", int(discount) / 100)
            products_workbook.write(f"E{idx}", product_url)
            idx += 1
        else:
            continue

    print(f"Page #{page} products information obtained correctly")

workbook.close()

print("File created sucessfully")