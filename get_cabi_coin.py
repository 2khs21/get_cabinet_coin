import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv
import random
import sys
import time


def setup_logger():
    """Set up logging configuration."""
    log_filename = os.path.join(os.path.dirname(__file__), "cabi_coin_log.txt")
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filemode="w"
    )


def load_credentials():
    """Load credentials from .env file."""
    env_path = os.path.join(os.path.dirname(__file__), "credentials.env")
    load_dotenv(env_path)

    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    if not username or not password:
        logging.error("Environment variables for USERNAME or PASSWORD are not set.")
        raise ValueError("Environment variables for USERNAME or PASSWORD are not set.")
    return username, password


def setup_driver():
    """Set up Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment to run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())

    return webdriver.Chrome(service=service, options=options)


def verify_current_url(driver, expected_url, timeout=5):
    """Verify if the current URL matches the expected URL."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.current_url.startswith(expected_url)
        )
        logging.info("URL verification successful.")
    except TimeoutException:
        current_url = driver.current_url
        error_message = f"Error: Current URL is {current_url}, but expected {expected_url}."
        logging.error(error_message)
        raise WebDriverException(error_message)


def login_to_cabi(driver, username, password):
    """Perform login to the Cabi website."""
    try:
        driver.get("https://cabi.42seoul.io/home")
        logging.info("Accessed Cabi home page.")

        # Click login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '42 Seoul 로그인')]"))
        )
        login_button.click()
        logging.info("Login button clicked.")

        # Enter login credentials
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_input.send_keys(username)
        logging.info("Username entered.")

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_input.send_keys(password)
        logging.info("Password entered.")

        # Submit login
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "login"))
        )
        login_button.click()
        logging.info("Login submitted.")

        # Verify login success
        verify_current_url(driver, "https://cabi.42seoul.io/home")
        logging.info("Login successful.")
    except Exception as e:
        logging.error(f"Login failed: {e}")
        sys.exit("Login failed. Check logs for details.")


def collect_coins(driver):
    """Navigate to the store page and attempt to collect coins."""
    try:
        driver.get("https://cabi.42seoul.io/store")
        logging.info("Navigated to the store page.")

        # Click the '동전 주우러가기' button
        coin_start_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '동전 주우러가기')]"))
        )
        coin_start_button.click()
        logging.info("Clicked '동전 주우러가기' button.")

        # Activate overlay
        driver.execute_script(
            "document.querySelector('.WrapperStyled-sc-1r1ff4e-0.iPbizH').classList.add('on');"
        )
        logging.info("Overlay activated.")

        # Wait for '줍기' button
        coin_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '줍기')]"))
        )
        coin_button.click()
        time.sleep(3)

        logging.info("Coin collected successfully.")

    except TimeoutException:
        logging.error("Timeout while trying to collect coins.")
        print("Error: Timeout while trying to collect coins.")
    except Exception as e:
        logging.error(f"Error during coin collection: {e}")
        print("Error during coin collection.")


def main():
    setup_logger()
    username, password = load_credentials()
    driver = setup_driver()

    try:
        # Perform login
        login_to_cabi(driver, username, password)

        # Attempt to collect coins
        collect_coins(driver)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print("An unexpected error occurred. Check the log for details.")

    finally:
        driver.quit()
        logging.info("Browser closed.")
        print("Script execution finished.")


if __name__ == "__main__":
    main()