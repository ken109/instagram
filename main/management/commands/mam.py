from django.core.management.base import BaseCommand

import traceback

from main.modules.mam import MamSpider
from main.modules.notify import ChatWork


class Command(BaseCommand):
    help = 'crawl Instagram mam'

    def handle(self, *args, **options):
        bot = MamSpider()
        chat = ChatWork()
        try:
            bot.start()
        except:
            bot.driver.save_screenshot('mam_error.png')
            chat.send(f"GET MAM\ntag: {bot.tag}\npost: {bot.url}\n{traceback.format_exc()}", image='mam_error.png')
            traceback.print_exc()
        finally:
            bot.quit()
