import re

from django.utils import timezone
from instagram.settings import TITLE

from main.models import Account, SearchWord

from .crawler import Crawler
from .notify import ChatWork


class MamSpider(Crawler):
    BASE_URL = 'https://www.instagram.com/'

    def __init__(self):
        super().__init__()

    def start(self):
        # self.login()
        while True:
            words = SearchWord.objects.order_by('-score').all()[:100]
            if len(words):
                min_count = sorted(words, key=lambda tag: tag.search_count)[0].search_count
                for word in words:
                    if word.search_count == min_count:
                        word.searched_at = timezone.now()
                        word.search_count += 1
                        word.save()
                        for post_from_word in self.posts_from_word(False,
                                                                   MamSpider.BASE_URL + 'explore/tags/' + word.word + '/'):
                            user_url, posts_from_user = self.user_posts_from_word_post(post_from_word)
                            for post_from_user in posts_from_user:
                                self.scoring(user_url, post_from_user)
                        break

    def user_posts_from_word_post(self, post):
        self.url = post
        self.driver.get(post)
        self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a').click()
        name = self.wait.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/*[1]').text
        img = self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/div/div/span/img').get_attribute('src')
        follower = self.wait.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title').replace(',', '')
        follower = int(follower) if re.match('^[0-9]*$', follower) else 0
        follow = self.wait.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text.replace(',', '')
        follow = int(follow) if re.match('^[0-9]*$', follow) else 0

        if Account.objects.filter(url=self.driver.current_url).exists():
            if Account.objects.get(url=self.driver.current_url).invisible == 1:
                return self.driver.current_url, []

        if follower > 3000 or 'official' in name:
            return self.driver.current_url, []
        ChatWork.send_message('{}:new'.format(TITLE))
        Account.objects.update_or_create(url=self.driver.current_url, defaults={
            'name': name,
            'img': img,
            'follower': follower,
            'follow': follow,
            'scored_at': timezone.now()
        })
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
