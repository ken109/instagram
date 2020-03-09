from django.utils import timezone

import time

from main.models import Account, SearchWord

from .crawler import Crawler


class MamSpider(Crawler):
    BASE_URL = 'https://www.instagram.com/'

    def __init__(self):
        super().__init__()

    def start(self):
        # self.login()
        while True:
            words = SearchWord.objects.order_by('-score').all()[:100]
            if not len(words):
                time.sleep(5)
            for word in words:
                word.searched_at = timezone.now()
                word.save()

                for post_from_word in self.posts_from_word(MamSpider.BASE_URL + 'explore/tags/' + word.word + '/'):
                    user_url, posts_from_user = self.user_posts_from_word_post(post_from_word)
                    for post_from_user in posts_from_user:
                        self.scoring(user_url, post_from_user)

    def user_posts_from_word_post(self, post):
        self.url = post
        self.driver.get(post)
        self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a').click()
        name = self.wait.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/*[1]').text
        img = self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/div/div/span/img').get_attribute('src')
        if not Account.objects.filter(url=self.driver.current_url):
            Account.objects.create(url=self.driver.current_url, name=name, img=img)
        posts = []
        for row in range(3):
            exist = True
            for col in range(3):
                element = self.driver.find_element_by_xpath(
                    f'//*[@id="react-root"]/section/main/div/div[@class=" _2z6nI"]/article/div[1]/div/div[{row + 1}]/div[{col + 1}]/a')
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
        self.url = post
        self.driver.get(post)
        try:
            text = self.wait.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/*[2]').text
            score = self.score(text)
            user = Account.objects.get(url=user_url)
            user.score += score
            user.save()
        except AttributeError:
            pass
