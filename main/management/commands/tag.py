from django.core.management.base import BaseCommand

import traceback

from main.modules.tag import TagSpider
from main.modules.notify import mail, ChatWork


class Command(BaseCommand):
    help = 'crawl Instagram tag'

    def handle(self, *args, **options):
        bot = TagSpider()
        chat = ChatWork()
        try:
            bot.start()
        except:
            mail('GET TAG', f"tag: {bot.tag}\n\npost: {bot.url}\n\n{traceback.format_exc()}")
            chat.send(f"GET TAG\n\ntag: {bot.tag}\n\npost: {bot.url}\n\n{traceback.format_exc()}")
            traceback.print_exc()
        finally:
            bot.quit()
