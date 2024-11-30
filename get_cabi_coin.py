import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from dotenv import load_dotenv


import random
import time

# 랜덤 대기 시간 설정 (예: 5초 ~ 15초 사이)
random_wait = random.uniform(5, 15)  # 5.0초에서 15.0초 사이의 랜덤 시간
print(f"Waiting for {random_wait:.2f} seconds before execution...")
time.sleep(random_wait)

print("Starting script execution...")

# ----- 시작 ------ 

# 1. 로그 설정
log_filename = "cabi_coin_log.txt"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 2. 환경 변수 로드
load_dotenv("credentials.env")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
if not USERNAME or not PASSWORD:
    logging.error("Environment variables for USERNAME or PASSWORD are not set.")
    raise ValueError("Environment variables for USERNAME or PASSWORD are not set.")


# 3. 브라우저 설정
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 브라우저를 숨김 모드로 실행
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 4. 드라이버 생성
driver = webdriver.Chrome(options=options)

try:
    # Google에 접속
    driver.get("https://cabi.42seoul.io/home")
    logging.info("Accessed Cabi home page.")

    # 로그인 버튼 클릭
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='L O G I N']"))
    )
    login_button.click()
    logging.info("Login button clicked.")

    # 42 로그인 입력
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    username_input.send_keys(USERNAME)
    logging.info("Username entered.")

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_input.send_keys(PASSWORD)
    logging.info("Password entered.")

    # 로그인 버튼 클릭
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "login"))
    )
    login_button.click()
    logging.info("Login submitted.")

    # 동전 줍기 버튼 클릭
    try:
        coin_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '줍기')]"))
        )
        coin_button.click()
        logging.info("Coin collected successfully!")
    except TimeoutException:
        logging.error("Login failed OR Coin button not found within the timeout period.")
    
    coin_button.click()
    logging.info("Coin collected successfully!")

    print("Coin collected successfully!")

except Exception as e:
    logging.error(f"An error occurred: {e}")
    print("An error occurred. Check the log for details.")

finally:
    driver.quit()
    logging.info("Browser closed.")
    print("END")