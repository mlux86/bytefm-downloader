import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from download import get_json


class ByteFmEpisode:
    mp3_api_call_url = 'return window.performance.getEntries().map(x => x.name)' \
                       '.filter(x => x.includes(\'/api/v1/broadcasts/\'))'
    mp3_base_path = 'https://archiv.byte.fm'

    def __init__(self, driver: WebDriver):
        self.driver = driver
        time.sleep(2)

    def get_mp3_urls(self):
        api_urls = self.driver.execute_script(self.mp3_api_call_url)
        if len(api_urls) > 1:
            raise Exception('Found more than one suitable API URLs')
        result = []
        json = get_json(api_urls[0], self.driver.get_cookies())
        return [*map(lambda recording: self.mp3_base_path + recording['url'], json['recordings'])]


class ByteFmShow:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def go_to_latest_episode(self):
        url = self.get_episodes_urls()[0]
        self.driver.get(url)
        return ByteFmEpisode(self.driver)

    def get_episodes_urls(self):
        links: list[WebElement] = self.driver.find_elements(By.CSS_SELECTOR, 'div.show-list-item__play a')
        return [*map(lambda elem: elem.get_attribute('href'), links)]


class ByteFm:
    login_url = 'https://www.byte.fm/freunde/login/'
    show_url = 'https://www.byte.fm/sendungen/{show}/'

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.driver.get(self.login_url)

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, 'button[type=\'submit\']').click()
        time.sleep(3)
        return self

    def go_to_program(self, show_name):
        self.driver.get(self.show_url.format(show=show_name))
        return ByteFmShow(self.driver)
