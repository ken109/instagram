from django.core.management.base import BaseCommand

import traceback

from main.modules import crawler


class Command(BaseCommand):
    help = 'crawl Instagram'

    def handle(self, *args, **options):
        bot = crawler.MomSpider()
        try:
            bot.start()
        except:
            traceback.print_exc()
        finally:
            bot.quit()
