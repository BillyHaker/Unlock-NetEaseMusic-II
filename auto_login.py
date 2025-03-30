# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00FFB78925C912712526C75F9D98947F5964B21FC655A9BEE884CCB74939D522AB21E76D6FC32ECDA2F4D92E017FD422439E003E4A530028FC1067871D699EAFF1E1AE5FC67A2F99C0E59EB28CC3434C98C34C08549B5F97625397698BF404C286761D4CF8BD30FADBE0830229B2BABA0480000AC68E277EBCF8D3F924B1606CA383BAC45A3D59BADB0D6DCD8E87F08B0615EC93BDE747E575E46169331ECB720C6EAF147B9B3D1ABBF27FAF12769C2F176255E968EBCC0191D5D41CE2F4681832650C80DEC65E38A5E663778198FC15B3C512985A0A1C77D7EF53A0EBDE25D40D5F73D8A271709CBA3135C175F656295F176AEFF3CE4A8492BE556C3E0D5F8B2295D88DC5EE2501DBAF72E8B78ECD2F38B3A41C195A36AB92C238B6C88BF53B5050A44F0269C22B06812CCA1368A2CCF104B53C70F51F4AB4D4DCAA51F96EE91DA907CCF0C94A58D0CEDB9CFA88895CBBE1D5E3F46CB8997532D02DDA23FCD24060204062F54B9C4CA58D17DBB3DBC96A"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
