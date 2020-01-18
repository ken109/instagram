from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import traceback

DEFAULT_DELAY = 50


def until_success(func):
    def wrapper(*args, **kwargs):
        count = 0
        while True:
            try:
                count += 1
                return func(*args, **kwargs)
            except:
                print(args, kwargs)
                traceback.print_exc()
                if count > 5:
                    break

    return wrapper


class Wait:
    def __init__(self, driver):
        self.driver = driver

    def wait_all(self, wait_time=DEFAULT_DELAY):
        time.sleep(wait_time * random.uniform(0.5, 1.5))
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located)

    @until_success
    def find_element_by_xpath(self, xpath, multiple=False, index=0, wait_time=DEFAULT_DELAY, data={}):
        self.wait_all(wait_time)
        if multiple:
            return self.driver.find_elements_by_xpath(xpath)[index]
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

    @until_success
    def find_element_by_name(self, name, multiple=False, index=0, wait_time=DEFAULT_DELAY):
        self.wait_all(wait_time)
        if multiple:
            return self.driver.find_elements_by_name(name)[index]
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, name)))

    @until_success
    def find_element_by_id(self, id, multiple=False, index=0, wait_time=DEFAULT_DELAY):
        self.wait_all(wait_time)
        if multiple:
            return self.driver.find_elements_by_id(id)[index]
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, id)))

    @until_success
    def find_element_by_class_name(self, class_name, multiple=False, index=0, wait_time=DEFAULT_DELAY):
        self.wait_all(wait_time)
        if multiple:
            return self.driver.find_elements_by_class_name(class_name)[index]
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
