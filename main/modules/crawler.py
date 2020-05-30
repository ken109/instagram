import chromedriver_binary

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

import time

from main.models import ScoreWord

from .wait import Wait
from .browser import Browser


def get_chrome_options():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-desktop-notifications')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--no-sandbox')
    return options


class Crawler:
    BASE_URL = 'https://www.instagram.com/'

    def __init__(self):
        self.driver = webdriver.Chrome(options=get_chrome_options())
        self.driver.implicitly_wait(10)
        self.wait = Wait(self.driver)
        self.browser = Browser(self.driver)
        self.tag = ''
        self.url = ''

    def login(self):
        self.driver.get(self.BASE_URL)
        self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input',
            wait_time=10).send_keys(
            'kubok.dev+instagram@gmail.com')
        self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input',
            wait_time=10).send_keys(
            'Kubo109Ken')
        self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button', wait_time=10).click()
        time.sleep(10)
        # self.wait.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()

    def posts_from_word(self, is_tag, word):
        self.tag = word
        self.driver.get(word)
        time.sleep(5)
        posts = []
        for row in range(3):
            for col in range(3):
                try:
                    if is_tag:
                        element = self.driver.find_element_by_xpath(
                            f'//*[@id="react-root"]/section/main/article/div[1]/div/div/div[{row + 1}]/div[{col + 1}]/a')
                    else:
                        element = self.driver.find_element_by_xpath(
                            f'//*[@id="react-root"]/section/main/article/div[2]/div/div[{row + 1}]/div[{col + 1}]/a')
                    self.browser.scroll_to_element(element)
                    posts.append(element.get_attribute('href'))
                except NoSuchElementException:
                    break

        return posts

    def score(self, text):
        score = 0
        for score_word in ScoreWord.objects.all():
            score += text.count(score_word.word) * score_word.score
        try:
            img = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/div[1]/div/div').find_element_by_tag_name('img')
            if 'one or more people' in img.get_attribute('alt'):
                score *= 2
        except NoSuchElementException:
            pass
        return score

    def quit(self):
        self.driver.close()
        self.driver.quit()
