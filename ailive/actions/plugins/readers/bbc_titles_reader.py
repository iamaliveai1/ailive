import logbook
import requests
from bs4 import BeautifulSoup

from ailive.actions.plugins.base import AlivePlugin

_logger = logbook.Logger(__name__)


class AliveBBCNewsPlugin(AlivePlugin):
    def __init__(self, scrape_recent_news=False):
        """
        :param scrape_recent_news: if True, the plugin will scrape all the news article titles on the page.
        If False, it will only scrape the news article titles that were posted since plugin was started.
        """
        super().__init__()
        self.can_post = False
        # specify the URL of the news website you want to scrape
        self.url = 'https://www.bbc.com/news'
        self.news = []
        self.scrape_recent_news = scrape_recent_news
        if self.scrape_recent_news:
            self.recently_handled_news = []
        else:
            self.recently_handled_news = self._pull_titles()

    def get_notifications(self):
        """
        This method return the recent news article titles.
        It tries to return each title only once.
        :return: list of news article titles
        """
        if not self.news:
            # if there are no news article titles in the list, pull the latest ones
            self.news = [
                title
                for title in self._pull_titles()
                if title not in self.recently_handled_news
            ]

        if not self.news:
            _logger.info("no new news")
            return []

        _logger.info(f"news: {self.news}")
        # remove and return the oldest news article title
        oldest_item = self.news.pop(0)

        if oldest_item in self.recently_handled_news:
            _logger.info(f"news item already handled: {oldest_item}")
            return []

        self.recently_handled_news.append(oldest_item)
        if len(self.recently_handled_news) > 20:
            self.recently_handled_news = self.recently_handled_news[-20:]
        return [oldest_item]

    def _pull_titles(self):
        # send a request to the website and get the HTML response
        response = requests.get(self.url)

        # create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # find all the news article titles on the page
        titles = soup.find_all('h3', class_='gs-c-promo-heading__title')

        # print out the titles
        _logger.info("titles: ")
        for title in titles:
            _logger.info(title.get_text())

        return [title.get_text() for title in titles]
