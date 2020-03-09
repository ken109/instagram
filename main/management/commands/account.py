from django.core.management.base import BaseCommand

import traceback
import os

from instagram.settings import TITLE

from main.modules.mam import MamSpider
from main.modules.notify import ChatWork


class Command(BaseCommand):
    help = 'crawl Instagram instagram'

    def handle(self, *args, **options):
        bot = MamSpider()
        try:
            bot.start()
        except:
            bot.driver.save_screenshot('account_error.png')
            ChatWork.send_file('account_error.png', f"{TITLE}\nGET ACCOUNT\ntag: {bot.tag}\npost: {bot.url}\n{traceback.format_exc()}")
            os.remove('account_error.png')
            traceback.print_exc()
        finally:
            bot.quit()
