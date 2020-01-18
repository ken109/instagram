from django.core.management.base import BaseCommand
from django.core.mail import send_mail

import traceback

from main.modules import tag


class Command(BaseCommand):
    help = 'crawl Instagram tags'

    def handle(self, *args, **options):
        bot = tag.TagSpider()
        try:
            bot.start()
        except:
            send_mail('停止', "tag\n" + traceback.format_exc(), 'papamama.insta@ctag-aws', ["kubok.dev@gmail.com"])
            traceback.print_exc()
        finally:
            bot.quit()
