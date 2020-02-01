from django.core.management.base import BaseCommand

import traceback

from main.modules.tag import TagSpider
from main.modules.notify import ChatWork


class Command(BaseCommand):
    help = 'crawl Instagram tag'

    def handle(self, *args, **options):
        bot = TagSpider()
        chat = ChatWork()
        try:
            bot.start()
        except:
            chat.send(f"GET TAG\ntag: {bot.tag}\npost: {bot.url}\n{traceback.format_exc()}")
            traceback.print_exc()
        finally:
            bot.quit()
