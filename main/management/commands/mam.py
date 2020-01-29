from django.core.management.base import BaseCommand
from django.core.mail import send_mail

import traceback

from main.modules import mam


class Command(BaseCommand):
    help = 'crawl Instagram mam'

    def handle(self, *args, **options):
        bot = mam.MomSpider()
        try:
            bot.start()
        except:
            send_mail('停止 MAM', f"mam\n{bot.url}\n{traceback.format_exc()}", 'papamama.insta@ctag-aws', ["kubok.dev@gmail.com"])
            traceback.print_exc()
        finally:
            bot.quit()
