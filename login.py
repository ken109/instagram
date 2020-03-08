from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
from main.modules.notify import ChatWork

options = Options()
options.add_argument('--headless')
options.add_argument("--user-data-dir=chrome-data")
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)

driver.get('https://www.instagram.com/')
ChatWork.send_screen(driver)

driver.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input').send_keys(
    'kubok.dev+instagram@gmail.com')
ChatWork.send_screen(driver)

driver.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input').send_keys(
    'Kubo109Ken')
ChatWork.send_screen(driver)

driver.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button').click()
time.sleep(10)
ChatWork.send_screen(driver)
