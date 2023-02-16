import os, time, random
import xlsxwriter
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
products_workbook = workbook.add_worksheet(name="Products-list")
products_workbook.write("A1", "Product title")
products_workbook.write("B1", "Discounted price")
products_workbook.write("C1", "Original price")
products_workbook.write("D1", "Discount")
products_workbook.write("E1", "Product URL")

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

        try:
            product_title = product.find_element(By.CLASS_NAME,
                                                 'promotion-item__title').text
        except Exception as e:
            print("There was an error getting the title of the product")

        try:
            original_price = product.find_element(
                By.CLASS_NAME,
                "andes-money-amount-combo__previous-value").find_element(
                    By.CLASS_NAME, "andes-money-amount__fraction").text
            original_price = original_price.replace(",", "")
        except Exception as e:
            print(
                f"There was an error getting the original price for {product_title}"
            )

        try:
            discounted_price = product.find_element(
                By.CLASS_NAME,
                "andes-money-amount--cents-superscript").find_element(
                    By.CLASS_NAME, "andes-money-amount__fraction").text
            discounted_price = discounted_price.replace(",", "")
        except Exception as e:
            print(
                f"There was an error getting the discounted price for {product_title}"
            )

        try:
            discount = product.find_element(
                By.CLASS_NAME, "andes-money-amount__discount").text[0:2]
            discount = discount.strip("% OFF")
        except Exception as e:
            print(
                f"There was an error getting the discount percentage for {product_title}"
            )

        try:
            product_url = product.find_element(
                By.CLASS_NAME,
                "promotion-item__link-container").get_attribute("href")
        except Exception as e:
            print(
                f"There was an error getting the product URL for {product_title}"
            )

        products_workbook.write(f"A{idx}", product_title)
        products_workbook.write(f"B{idx}", int(original_price))
        products_workbook.write(f"C{idx}", int(discounted_price))
        products_workbook.write(f"D{idx}", int(discount) / 100)
        products_workbook.write(f"E{idx}", product_url)
        idx += 1

    print(f"Page #{page} products information obtained correctly")

workbook.close()

print("File created sucessfully")