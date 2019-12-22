from django.core.management.base import BaseCommand

import traceback

from main.modules import tag


class Command(BaseCommand):
    help = 'crawl Instagram tags'

    def handle(self, *args, **options):
        bot = tag.TagSpider()
        try:
            bot.start()
        except:
            traceback.print_exc()
        finally:
            bot.quit()
