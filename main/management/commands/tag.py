from django.core.management.base import BaseCommand

import traceback

from main.modules.tag import TagSpider
from main.modules.notify import mail


class Command(BaseCommand):
    help = 'crawl Instagram tag'

    def handle(self, *args, **options):
        bot = TagSpider()
        try:
            bot.start()
        except:
            mail('GET TAG', f"{bot.url}\n{traceback.format_exc()}")
            traceback.print_exc()
        finally:
            bot.quit()
