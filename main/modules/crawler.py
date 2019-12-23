from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .wait import Wait
from .browser import Browser


class Crawler:
    BASE_URL = 'https://www.instagram.com/'

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)
        self.driver.implicitly_wait(10)
        self.wait = Wait(self.driver)
        self.browser = Browser(self.driver)

    def login(self):
        self.driver.get(self.BASE_URL)
        self.wait.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a',
                                        wait_time=2).click()
        self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input',
            wait_time=1).send_keys(
            'ikegawa@spotakabiz.co.jp')
        self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input',
            wait_time=1).send_keys(
            'meimaki0419')
        self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button', wait_time=1).click()
        # self.wait.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()

    def posts_from_word(self, word):
        self.wait.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(word)
        self.wait.find_element_by_xpath(
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]').click()
        posts = []
        for row in range(3):
            for col in range(3):
                element = self.driver.find_element_by_xpath(
                    f'//*[@id="react-root"]/section/main/article/div[1]/div/div/div[{row + 1}]/div[{col + 1}]/a')
                self.browser.scroll_to_element(element)
                posts.append(element.get_attribute('href'))
        return posts
