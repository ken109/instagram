from django.core.management.base import BaseCommand

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

from main.models import Account


class Command(BaseCommand):
    help = 'update profile'

    def handle(self, *args, **options):
        accounts = Account.objects.order_by('-score')[99:]
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--user-data-dir=chrome-data")
        driver = webdriver.Chrome(chrome_options=chrome_options)

        for account in accounts:
            driver.get(account.url)
            account.img = driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/div/div/span/img').get_attribute('src')
            follower = driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title').replace(
                ',', '')
            account.follower = int(follower) if re.match('^[0-9]*$', follower) else 0
            follow = driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text.replace(',', '')
            account.follow = int(follow) if re.match('^[0-9]*$', follow) else 0
            account.save()
            time.sleep(60)

        driver.close()
        driver.quit()
