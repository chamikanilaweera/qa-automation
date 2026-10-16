from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    FINISH_BTN = (By.CSS_SELECTOR, "[data-test='finish'], #finish")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header'], .complete-header")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def fill_details(self, first, last, postal):
        values = {
            self.FIRST_NAME: first,
            self.LAST_NAME: last,
            self.POSTAL_CODE: postal,
        }

        def all_fields_filled(driver):
            filled = True
            for locator, text in values.items():
                element = driver.find_element(*locator)
                if element.get_attribute("value") != text:
                    element.clear()
                    element.send_keys(text)
                    filled = False
            return filled

        self.wait.until(
            all_fields_filled,
            message="Form fields did not keep the typed values (page keeps resetting them)",
        )
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BTN)).click()
        self.wait.until(
            EC.url_contains("checkout-step-two"),
            message="Did not reach checkout-step-two after clicking Continue",
        )

    def finish_order(self):
        self.wait.until(EC.element_to_be_clickable(self.FINISH_BTN)).click()

    def get_confirmation(self):
        return self.wait.until(EC.visibility_of_element_located(self.COMPLETE_HEADER)).text