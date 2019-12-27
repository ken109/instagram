from django.utils import timezone

import time

from main.models import Account, SearchWord, ScoreWord

from .crawler import Crawler


class MomSpider(Crawler):
    BASE_URL = 'https://www.instagram.com/'

    def __init__(self):
        super().__init__()

    def start(self):
        self.login()
        while True:
            word = SearchWord.objects.filter(searched_at__isnull=True, scored_at__isnull=False).order_by('-score').first()
            if word is None:
                time.sleep(5)
            else:
                word.searched_at = timezone.now()
                word.save()
                for post_from_word in self.posts_from_word('#' + word.word):
                    user_url, posts_from_user = self.user_posts_from_word_post(post_from_word)
                    for post_from_user in posts_from_user:
                        self.scoring(user_url, post_from_user)

    def user_posts_from_word_post(self, post):
        self.driver.get(post)
        self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[1]/h2/a').click()
        name = self.wait.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h1').text
        img = self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/div/div/span/img').get_attribute('src')
        if not Account.objects.filter(url=self.driver.current_url):
            Account.objects.create(url=self.driver.current_url, name=name, img=img)
        posts = []
        for row in range(3):
            exist = True
            for col in range(3):
                element = self.driver.find_element_by_xpath(
                    f'//*[@id="react-root"]/section/main/div/div[@class=" _2z6nI"]/article[2]/div[1]/div/div[{row + 1}]/div[{col + 1}]/a')
                if element is not None:
                    self.browser.scroll_to_element(element)
                    posts.append(element.get_attribute('href'))
                else:
                    exist = False
                    break
            if not exist:
                break
        return self.driver.current_url, posts

    def scoring(self, user_url, post):
        self.driver.get(post)
        text = self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span',
            data={'user_url': user_url, 'post': post}).text
        score = 0
        for score_word in ScoreWord.objects.all():
            score += text.count(score_word.word) * score_word.score
        user = Account.objects.get(url=user_url)
        user.score += score
        user.save()
