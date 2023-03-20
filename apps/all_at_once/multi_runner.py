from time import sleep

import logbook
from dynaconf import Dynaconf

from ailive.engine.chatgpt.prompts.funny_prompts import jerry_seinfeld_prompt, louis_ck_prompt
from apps.funny_news_reactor.jerry_seinfeld_reactor import NewsReactor as JerrySeinfeldNewsReactor
from apps.funny_news_reactor.louis_ck_reactor import NewsReactor as LouisCKNewsReactor
from revChatGPT.typing import Error

_logger = logbook.Logger(__name__)

settings = Dynaconf(
    envvar_prefix="FUNNY_NEWS",
    settings_files=['settings.yaml', '.secrets.yaml'],
)


def get_bots():
    seinfeld_news_reactor = JerrySeinfeldNewsReactor(
        prompt=jerry_seinfeld_prompt,
        v_name="Jerry Seinfeld GPT",
        version=settings.chatgpt.version,
        sleep_seconds=10)

    louis_ck_news_reactor = LouisCKNewsReactor(
        prompt=louis_ck_prompt,
        v_name="Louis CK GPT",
        version=settings.chatgpt.version,
        sleep_seconds=60)

    return [seinfeld_news_reactor, louis_ck_news_reactor]


class MultiRunner:
    def __init__(self, bots):
        self.bots = bots
        self.sleep_seconds = max(bot.sleep_seconds for bot in bots)

    def run_forever(self):
        _logger.info("starting endless loop conversation...")
        while True:
            try:
                for bot in self.bots:
                    bot.run_once()
            except (ValueError, Error) as e:
                _logger.error(f"error: {e}", exc_info=True)
                _logger.info(f"sleeping for {self.sleep_seconds} seconds...")
                sleep(self.sleep_seconds)
            # accept KeyboardInterrupt
            except KeyboardInterrupt:
                _logger.info("stopping AiLive application")
                break


def main():
    bots = get_bots()
    multi_runner = MultiRunner(bots)
    multi_runner.run_forever()


if __name__ == '__main__':
    main()
