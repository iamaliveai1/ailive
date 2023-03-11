import json

import logbook
import requests
from requests.auth import HTTPBasicAuth

from ailive.actions.plugins.base import AlivePlugin
from ailive.engine.chatgpt.chatgpt_api import ask_gpt, get_new_chatbot
from ailive.engine.chatgpt.prompts.formatting_prompts import html_formatter_prompts

_logger = logbook.Logger(__name__)


class WordPressAlivePlugin(AlivePlugin):
    can_post = True

    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url
        self.url = f"{self.base_url}/wp-json/wp/v2/posts"
        self.auth = HTTPBasicAuth(username, password) if username and password else None
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        # use the chatbot to format the content
        self.chatbot = get_new_chatbot()

    def create_post(self, title, content):
        # format the content
        formatted_content = ask_gpt(html_formatter_prompts + content, chatbot=self.chatbot)
        payload = json.dumps({
            "status": "publish",
            "title": title,
            "content": formatted_content,
        })
        _logger.info(f"posting to url: {self.url}")
        _logger.info(f"payload: {payload}")
        response = requests.post(self.url, data=payload, headers=self.headers, auth=self.auth)
        _logger.info(f"response from url: {response.status_code}")
        _logger.info(f"response data: {response.json()}")
        print(response)
        return response

    def delete_page(self, page_id):
        """
        Delete a page, mainly used for testing
        :param page_id:
        :return:
        """
        response = requests.request(
            "DELETE",
            self.url + f"/{page_id}",
            headers=self.headers,
            auth=self.auth
        )
        _logger.info(response)
        _logger.info(response.json())
        return response

