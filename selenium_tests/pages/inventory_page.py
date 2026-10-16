from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    TITLE = (By.CLASS_NAME, "title")
    ADD_TO_CART_BTNS = (By.CSS_SELECTOR, "button.btn_inventory")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    PRICES = (By.CLASS_NAME, "inventory_item_price")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_title(self):
        return self.wait.until(EC.visibility_of_element_located(self.TITLE)).text

    def add_first_item_to_cart(self):
        self.driver.find_elements(*self.ADD_TO_CART_BTNS)[0].click()

    def get_cart_count(self):
        return self.wait.until(EC.visibility_of_element_located(self.CART_BADGE)).text

    def sort_by(self, value):
        # value: "az", "za", "lohi", "hilo"
        dropdown = self.driver.find_element(*self.SORT_DROPDOWN)
        Select(dropdown).select_by_value(value)

    def get_prices(self):
        elements = self.driver.find_elements(*self.PRICES)
        return [float(e.text.replace("$", "")) for e in elements]

    def open_cart(self):
        self.driver.find_element(*self.CART_LINK).click()