from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_checkout_complete(driver):
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.add_first_item_to_cart()
    inventory.open_cart()

    cart = CartPage(driver)
    assert cart.get_item_count() == 1
    cart.click_checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_details("Chamika", "Nilaweera", "81000")
    checkout.finish_order()
    assert "Thank you for your order" in checkout.get_confirmation()