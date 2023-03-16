from abc import ABCMeta, abstractmethod
from datetime import datetime
from time import sleep

import logbook

from ailive.actions.executors import execute_social_media_func
from ailive.actions.plugins.base import AlivePlugin
from ailive.engine.chatgpt.chatgpt_api import ask_gpt
from ailive.engine.chatgpt.extractor import extract_args
from revChatGPT.V1 import Error

_logger = logbook.Logger(__name__)


class AiLive(metaclass=ABCMeta):

    def __init__(self, prompt, sleep_seconds=10, v_name="ChatGPT"):
        self.prompt = prompt
        self.sleep_seconds = sleep_seconds
        self.iteration = 0
        self.plugins = []
        self.journal = []
        self.last_notifications = []
        self.new_journal_size_threshold = 0
        self.prompts_initialized = False
        self.register_plugins(self.get_plugins())
        self.v_name = v_name

    @abstractmethod
    def get_plugins(self):
        """
        This method should be implemented by the child class
        It handles the plugins loading, thus defining the behavior of the application
        :return:
        """
        raise NotImplementedError

    def register_plugin(self, plugin: AlivePlugin):
        self.plugins.append(plugin)

    def register_plugins(self, plugin: list[AlivePlugin]):
        self.plugins.extend(plugin)

    def unregister_plugin(self, plugin: AlivePlugin):
        self.plugins.remove(plugin)

    def run_forever(self):
        _logger.info("starting endless loop conversation...")
        while True:
            try:
                self.run_once()
            except (ValueError, Error) as e:
                _logger.error(f"error: {e}", exc_info=True)
                self._sleep()
            # accept KeyboardInterrupt
            except KeyboardInterrupt:
                _logger.info("stopping AiLive application")
                break

    def run_once(self):
        if not self.prompts_initialized:
            self.init()
        # notify the AI engine about recent notifications
        answer = self.notify_notifications()
        if answer:
            self.execute_response(answer)
            self.manage_journal(answer)
        self._sleep()
        self.iteration += 1

    def init(self):
        """
        starts a conversation with ChatGPT by sending the initial prompt
        :return: the first answer from the AI engine
        """
        _logger.info("Starting AiLive application")
        _logger.info("#" * 50)
        _logger.info("Starting conversation with ChatGPT")
        _logger.info("#" * 50)
        answer = ask_gpt(self.prompt)
        assert answer and len(answer) > 0
        _logger.info(f"prompt created successfully")
        _logger.info(f"prompt response: {answer}")
        self.prompts_initialized = True

    def manage_journal(self, answer):
        """
        this method manages the journal of journey done by the AI engine
        it records its actions in a way that can be later used to post a blog
        :param answer:
        :return:
        """
        # update the journal with gpt response
        self.update_journal(message=f"{answer}")
        # count the total number of words in the journal
        total_words = sum([len(message.split()) for message in self.journal])
        if total_words > self.new_journal_size_threshold:
            self.post_journal()
            self.journal = []

    def _sleep(self):
        _logger.info(f"sleeping for {self.sleep_seconds} seconds...")
        sleep(self.sleep_seconds)

    def notify_notifications(self):
        self.last_notifications = self._collect_notifications()
        _logger.info(f"there are {len(self.last_notifications)} notifications")
        print(f"there are {len(self.last_notifications)} notifications")
        if not self.last_notifications:
            return None
        message = f"{self.last_notifications}"
        # self.update_journal(message=message)
        # push the notifications to the AI engine
        answer = ask_gpt(message)
        return answer

    def _collect_notifications(self):
        """
        this method collects notifications from all the channels by triggering
        the appropriate plugins and collecting the notifications
        :return:
        """
        notifications = []
        for plugin in self.plugins:
            plugin_notifications = plugin.get_notifications()
            _logger.info(f"collected {len(plugin_notifications)} notifications from {plugin}")
            print(f"collected {len(plugin_notifications)} notifications from {plugin}")
            notifications.extend(plugin_notifications)
        return notifications

    @staticmethod
    def execute_response(answer):
        """
        this method executes the response from the AI engine by extracting the
        actions and executing them
        :param answer:
        :return:
        """
        _logger.info(f"executing response: {answer}")

        for action in answer.split("\n"):
            if "(" not in action:
                continue
            _logger.info(f"executing action: {action}")
            func_name, args = extract_args(action)
            execute_social_media_func(func_name, args)

    def post_journal(self):
        _logger.info("posting journal to wordpress...")
        for plugin in self.plugins:
            if plugin.can_post:
                notifications_str = "\n".join(self.last_notifications)
                title = f'{datetime.now().strftime("%Y-%m-%d %H:%M")} {self.v_name} Reacts to "{notifications_str}"'
                plugin.create_post(
                    title=title,
                    content="<br><br>".join(self.journal)
                )

    def update_journal(self, message):
        _logger.info(f"updating internal journal with {message}")
        self.journal.append(message)
