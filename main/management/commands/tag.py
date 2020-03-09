from django.core.management.base import BaseCommand

import traceback
import os

from instagram.settings import TITLE

from main.modules.tag import TagSpider
from main.modules.notify import ChatWork


class Command(BaseCommand):
    help = 'crawl Instagram tag'

    def handle(self, *args, **options):
        bot = TagSpider()
        try:
            bot.start()
        except:
            bot.driver.save_screenshot('tag_error.png')
            ChatWork.send_file('tag_error.png', f"{TITLE}\nGET TAG\ntag: {bot.tag}\npost: {bot.url}\n{traceback.format_exc()}")
            os.remove('tag_error.png')
            traceback.print_exc()
        finally:
            bot.quit()
