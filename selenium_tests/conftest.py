import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

LOCAL_DRIVER = os.path.join(os.path.dirname(__file__), "chromedriver.exe")


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    })
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-popup-blocking")
    # prashnaya thawamath thiyenawanam meka uncomment karanna:
    # options.add_argument("--headless=new")
    if os.path.exists(LOCAL_DRIVER):
        driver = webdriver.Chrome(service=Service(LOCAL_DRIVER), options=options)
    else:
        driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            try:
                os.makedirs("screenshots", exist_ok=True)
                driver.save_screenshot(f"screenshots/{item.name}.png")
            except Exception:
                pass