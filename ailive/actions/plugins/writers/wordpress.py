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

    def __init__(self, base_url, username=None, password=None, categories=None, tags=None):
        self.base_url = base_url
        self.url = f"{self.base_url}/wp-json/wp/v2/posts"
        self.auth = HTTPBasicAuth(username, password) if username and password else None
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        # use the chatbot to format the content
        self.chatbot = get_new_chatbot()
        self.categories = categories if categories else []
        self.tags = tags if tags else []
        self.categories_data = []
        self.tags_data = []
        self.init()

    def init(self):
        _logger.info("initializing wordpress plugin")
        _logger.info(f"base_url: {self.base_url}")
        self._update_categories()
        self._update_tags()

    def _update_tags(self):
        # get the tags
        tags_url = f"{self.base_url}/wp-json/wp/v2/tags"
        response = requests.get(tags_url, headers=self.headers, auth=self.auth)
        if response.status_code != 200:
            _logger.error(f"error getting tags: {response.text}")
        else:
            self.tags_data = response.json()
        _logger.info(f"tags: {self.tags_data}")

    def _update_categories(self):
        # get the categories
        categories_url = f"{self.base_url}/wp-json/wp/v2/categories"
        response = requests.get(categories_url, headers=self.headers, auth=self.auth)
        if response.status_code != 200:
            _logger.error(f"error getting categories: {response.text}")
        else:
            self.categories_data = response.json()
        _logger.info(f"categories: {self.categories_data}")

    def _get_categories_ids(self, categories):
        # find the categories IDs according to the list
        existing_categories = [category["name"].lower() for category in self.categories_data]
        lower_categories = [category.lower() for category in categories]

        for category in lower_categories:
            if category not in existing_categories:
                # category not found, create it
                category_url = f"{self.base_url}/wp-json/wp/v2/categories"
                data = {
                    "name": category,
                }
                response = requests.post(category_url, headers=self.headers, auth=self.auth, data=json.dumps(data))
                if response.status_code != 201:
                    _logger.error(f"error creating category: {response.text}")
                    continue
                category_data = response.json()
                self.categories_data.append(category_data)

        categories_ids = list({category["id"] for category in self.categories_data if category["name"].lower() in lower_categories})
        _logger.info(f"categories_ids: {categories_ids}")
        return categories_ids

    def _get_tags_ids(self, tags):
        # find the tags IDs according to the list
        existing_tags = [tag["name"].lower() for tag in self.tags_data]
        lower_tags = [tag.lower() for tag in tags]

        for tag in lower_tags:
            if tag not in existing_tags:
                # tag not found, create it
                tag_url = f"{self.base_url}/wp-json/wp/v2/tags"
                data = {
                    "name": tag,
                }
                response = requests.post(tag_url, headers=self.headers, auth=self.auth, data=json.dumps(data))
                if response.status_code != 201:
                    _logger.error(f"error creating tag: {response.text}")
                    continue
                tag_data = response.json()
                self.tags_data.append(tag_data)

        tags_ids = list({tag["id"] for tag in self.tags_data if tag["name"].lower() in lower_tags})
        _logger.info(f"tags_ids: {tags_ids}")
        return tags_ids

    def create_post(self, title, content, categories=None, tags=None):
        # format the content
        formatted_content = ask_gpt(html_formatter_prompts + content, chatbot=self.chatbot)
        data = {
            "status": "publish",
            "title": title,
            "content": formatted_content,
        }
        categories = categories if categories else []
        gpt_categories = get_gpt_categories(content)
        all_categories = self.categories + categories + gpt_categories
        if all_categories:
            data["categories"] = self._get_categories_ids(all_categories)

        tags = tags if tags else []
        gpt_tags = get_gpt_tags(content)
        all_tags = self.tags + tags + gpt_tags
        if all_tags:
            data["tags"] = self._get_tags_ids(all_tags)

        payload = json.dumps(data)
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


def get_gpt_categories(content):
    """
    Get the categories from the content
    :param content:
    :return:
    """
    categories_prompt = "What categories do you want to add to this post? Give me the categories as a list of: catergory1, category2, … and nothing else. Post is:\n"
    gpt_categories = ask_gpt(categories_prompt + content, chatbot=get_new_chatbot())
    return gpt_categories.split(",")


def get_gpt_tags(content):
    """
    Get the tags from the content
    :param content:
    :return:
    """
    tags_prompt = "What tags do you want to add to this post? Give me the tags as a list of: tag1, tag2, … and nothing else. Post is:\n"
    gpt_tags = ask_gpt(tags_prompt + content, chatbot=get_new_chatbot())
    return gpt_tags.split(",")

