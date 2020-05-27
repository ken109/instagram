from django.core.management.base import BaseCommand

import chromedriver_binary
from selenium import webdriver
import time
import re

from main.models import Account
from main.modules.crawler import get_chrome_options


class Command(BaseCommand):
    help = 'update profile'

    def handle(self, *args, **options):
        accounts = Account.objects.filter(invisible=0).order_by('-score').all()[99:]
        driver = webdriver.Chrome(chrome_options=get_chrome_options())

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
