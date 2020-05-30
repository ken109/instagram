import chromedriver_binary

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from main.modules.notify import ChatWork


options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-desktop-notifications')
options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

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

driver.find_elements_by_css_selector('button')[1].click()
time.sleep(2)
ChatWork.send_screen(driver)

driver.close()
driver.quit()

# driver.find_element_by_css_selector('input').send_keys(input('6桁：'))
# time.sleep(2)
# ChatWork.send_screen(driver)
#
# driver.find_element_by_xpath(
#     '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button').click()
# time.sleep(2)
# ChatWork.send_screen(driver)
