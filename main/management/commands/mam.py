from django.core.management.base import BaseCommand

import traceback

from main.modules import mam


class Command(BaseCommand):
    help = 'crawl Instagram mams'

    def handle(self, *args, **options):
        bot = mam.MomSpider()
        try:
            bot.start()
        except:
            traceback.print_exc()
        finally:
            bot.quit()
