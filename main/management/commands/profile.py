from django.core.management.base import BaseCommand

import chromedriver_binary
import time
import re

from main.models import Account
from main.modules.crawler import Crawler
from main.modules.notify import ChatWork


class Command(BaseCommand):
    help = 'update profile'

    def handle(self, *args, **options):
        crawler = Crawler()
        crawler.login()
        accounts = Account.objects.filter(invisible=0).order_by('-score').all()[:99]

        for account in accounts:
            crawler.driver.get(account.url)
            try:
                ChatWork.send_screen(crawler.driver)
                account.img = crawler.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/header/div/div/span/img').get_attribute('src')
                follower = crawler.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title').replace(
                    ',', '')
                account.follower = int(follower) if re.match('^[0-9]*$', follower) else 0
                follow = crawler.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text.replace(',', '')
                account.follow = int(follow) if re.match('^[0-9]*$', follow) else 0
                account.save()
            except:
                pass
            time.sleep(40)

        crawler.driver.close()
        crawler.driver.quit()
