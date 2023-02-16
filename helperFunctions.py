from selenium.webdriver.common.by import By


def getProductTitle(product):
    try:
        return product.find_element(By.CLASS_NAME,
                                    'promotion-item__title').text
    except Exception as e:
        print("There was an error getting the title of the product")
        return None


def getOriginalPrice(product):
    try:
        original_price = product.find_element(
            By.CLASS_NAME,
            "andes-money-amount-combo__previous-value").find_element(
                By.CLASS_NAME, "andes-money-amount__fraction").text
        original_price = original_price.replace(",", "")
        return original_price
    except Exception as e:
        print(
            f"There was an error getting the original price for {getProductTitle(product)}"
        )
        return None


def getDiscountedPrice(product):
    try:
        discounted_price = product.find_element(
            By.CLASS_NAME,
            "andes-money-amount--cents-superscript").find_element(
                By.CLASS_NAME, "andes-money-amount__fraction").text
        discounted_price = discounted_price.replace(",", "")
        return discounted_price
    except Exception as e:
        print(
            f"There was an error getting the discounted price for {getProductTitle(product)}"
        )
        return None


def getDiscount(product):
    try:
        discount = product.find_element(
            By.CLASS_NAME, "andes-money-amount__discount").text[0:2]
        discount = discount.strip("% OFF")
        return discount
    except Exception as e:
        print(
            f"There was an error getting the discount percentage for {getProductTitle(product)}"
        )
        return None


def getProductUrl(product):

    try:
        return product.find_element(
            By.CLASS_NAME,
            "promotion-item__link-container").get_attribute("href")
    except Exception as e:
        print(
            f"There was an error getting the product URL for {getProductTitle(product)}"
        )
        return None


def validateProduct(product_title, original_price, discounted_price, discount,
                    product_url):
    if (product_title == None or original_price == None
            or discounted_price == None or discount == None
            or product_url == None):
        return False
    else:
        return True