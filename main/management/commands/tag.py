from django.core.management.base import BaseCommand

import traceback

from main.modules import tag
from main.modules.notify import mail


class Command(BaseCommand):
    help = 'crawl Instagram tag'

    def handle(self, *args, **options):
        bot = tag.TagSpider()
        try:
            bot.start()
        except:
            mail('停止 TAG', f"{bot.url}\n{traceback.format_exc()}", ["kubok.dev@gmail.com"])
            traceback.print_exc()
        finally:
            bot.quit()
