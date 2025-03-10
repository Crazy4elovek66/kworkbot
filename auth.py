from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle

EMAIL = "PixelPhantom"
PASSWORD = "onetuztv30"

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login_and_save_cookies():
    driver.get("https://kwork.ru/user/login")
    time.sleep(3)

    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.ENTER)
    time.sleep(5)

    with open("kwork_cookies.pkl", "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print("✅ Cookies сохранены в файл 'kwork_cookies.pkl'")

    driver.quit()

login_and_save_cookies()
