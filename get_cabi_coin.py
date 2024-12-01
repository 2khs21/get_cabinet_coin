import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import sys

import os
from dotenv import load_dotenv


import random
import time

# 랜덤 대기 시간 설정 (예: 5초 ~ 15초 사이)
random_wait = random.uniform(5, 15)  # 5.0초에서 15.0초 사이의 랜덤 시간
print(f"Waiting for {random_wait:.2f} seconds before execution...")
# time.sleep(random_wait)

print("Starting script execution...")

def verify_current_url(driver, expected_url, timeout=5):
    try:
        # URL이 로드될 때까지 대기
        WebDriverWait(driver, timeout).until(
            lambda d: d.current_url.startswith(expected_url)
        )
        logging.info("URL verification successful.")
        print("URL verification successful.")
    except TimeoutException:
        current_url = driver.current_url
        error_message = f"Error: Current URL is {current_url}, but expected {expected_url}."
        logging.error(error_message)
        raise WebDriverException(error_message)


# ----- 시작 ------ 

# 1. 로그 설정
log_filename = os.path.join(os.path.dirname(__file__), "cabi_coin_log.txt")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode="w"  # 기존 파일 덮어쓰기
)

# 스크립트의 경로를 기준으로 .env 파일 설정
env_path = os.path.join(os.path.dirname(__file__), "credentials.env")
load_dotenv(env_path)

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

    # 로그인 확인
    expected_url = "https://cabi.42seoul.io/home"
    try:
        verify_current_url(driver, expected_url)
    except WebDriverException as e:
        print("Login Failed")
        logging.error("Login Failed")
        sys.exit()
        


    # 동전 줍기 버튼 클릭
    try:
        driver.get("https://cabi.42seoul.io/store")
        coin_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '동전 주우러가기')]"))
        )
        coin_button.click()

        print("줍기시도!")
        coin_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '줍기')]"))
        )
        print("줍기 버튼 찾음")
        if coin_button.is_enabled():
            # 버튼이 활성화되어 있으면 클릭
            coin_button.click()
            logging.info("Coin button clicked successfully.")
        else:
            # 버튼이 비활성화되어 있으면 로그 기록
            logging.info("A already collected the coin")
            print("이미 주웠다!")

        # success_modal = WebDriverWait(driver, 3).until(
        #     EC.presence_of_element_located((By.XPATH, "//*[text()='동전 줍기 성공']"))
        # )

        # print ("동전 줍기 성공")
        # logging.info("Success : get coin")

    except Exception as e:
        # 성공 메시지가 나타나지 않으면 에러 처리
        logging.error(f"Coin collection failed or modal not found. Error: {e}")
        print("Error: Coin collection failed.")


except Exception as e:
    logging.error(f"An error occurred: {e}")
    print("An error occurred. Check the log for details.")

finally:
    driver.quit()
    logging.info("Browser closed.")
    print("Finish script")