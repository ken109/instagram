from django.core.management.base import BaseCommand

import traceback

from main.modules.mam import MamSpider
from main.modules.notify import mail, ChatWork


class Command(BaseCommand):
    help = 'crawl Instagram mam'

    def handle(self, *args, **options):
        bot = MamSpider()
        chat = ChatWork()
        try:
            bot.start()
        except:
            mail('GET MAM', f"tag: {bot.tag}\n\npost: {bot.url}\n\n{traceback.format_exc()}")
            chat.send(f"GET MAM\n\ntag: {bot.tag}\n\npost: {bot.url}\n\n{traceback.format_exc()}")
            traceback.print_exc()
        finally:
            bot.quit()
