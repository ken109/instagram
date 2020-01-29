from django.core.management.base import BaseCommand

import traceback

from main.modules import mam
from main.modules.notify import mail


class Command(BaseCommand):
    help = 'crawl Instagram mam'

    def handle(self, *args, **options):
        bot = mam.MomSpider()
        try:
            bot.start()
        except:
            mail('停止 MAM', f"{bot.url}\n{traceback.format_exc()}", ["kubok.dev@gmail.com"])
            traceback.print_exc()
        finally:
            bot.quit()
