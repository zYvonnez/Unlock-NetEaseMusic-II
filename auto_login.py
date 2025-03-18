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
    browser.add_cookie({"name": "MUSIC_U", "value": "0020EACC0D6F986F8D9627EC203CB5678AE0C0C7873E77E6A80558D91AEAE076BE9447CDD1D5AD56EC3A32D4015D67CD509C91881B7D544BA8E5178638EC4D845A94EA095CD4CB697E65BE6539404A504EAC908341805AA7AE8EC1E2F87768D22D65D98667831BEDF9508387B460026BE3165B175FA6DDE9D1B9F1FAC8F1EA9D41DDF9434D85B2740B20365915E399F51D2F0CB94D61CA70F7F7E2561C1C06CE1B0D688DE62606BC0DFFCDC60CCEB42D31A75B99DE7CD07054CA51DA5B03C45A3BA390FB0456A4D0C6717295BAD606199F0828FC886B62AAE7B4998800BC69101C65E5143752DAA1546718C61E86F86E6EB746737FBC3CA6BE0317D58277785C24634978BCAE2FBB414B7652930D362F0493A5263FD7B2F8CB0A944CEFC8C37EE278922ECC43C2C365C3D05454428CC96174279679FF8E42D4FAE7FD7F83D6EAE1EE5AC759617B624CC9445928C21F3CD72F5DC5669C99AF65848E527226076C4D"})
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
