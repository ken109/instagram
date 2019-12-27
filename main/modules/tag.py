from django.utils import timezone

import time
import re

from main.models import SearchWord, ScoreWord

from .crawler import Crawler


class TagSpider(Crawler):
    BASE_URL = 'https://www.instagram.com/'

    def __init__(self):
        super().__init__()

    def start(self):
        self.login()
        while True:
            word = SearchWord.objects.filter(scored_at__isnull=True).order_by('id').first()
            if word is None:
                time.sleep(5)
            else:
                word.scored_at = timezone.now()
                word.save()
                for post_from_word in self.posts_from_word('#' + word.word):
                    self.scoring(word.word, post_from_word)
                zero_words = SearchWord.objects.filter(score=0, scored_at__isnull=False).all()
                zero_words.delete()

    def scoring(self, word, post):
        self.driver.get(post)
        text = self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span',
            data={'word': word, 'post': post}).text
        tags = re.compile(r'#(\w+)').findall(text)
        for tag in tags:
            SearchWord.objects.update_or_create(word=tag)
        score = 0
        for score_word in ScoreWord.objects.all():
            score += text.count(score_word.word) * score_word.score
        word_ob = SearchWord.objects.get(word=word)
        word_ob.score += score
        word_ob.save()
