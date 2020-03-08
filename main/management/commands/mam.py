from django.core.management.base import BaseCommand

import traceback
import os

from main.modules.mam import MamSpider
from main.modules.notify import ChatWork


class Command(BaseCommand):
    help = 'crawl Instagram mam'

    def handle(self, *args, **options):
        bot = MamSpider()
        try:
            bot.start()
        except:
            bot.driver.save_screenshot('mam_error.png')
            ChatWork.send_file('mam_error.png', f"GET MAM\ntag: {bot.tag}\npost: {bot.url}\n{traceback.format_exc()}")
            os.remove('mam_error.png')
            traceback.print_exc()
        finally:
            bot.quit()
