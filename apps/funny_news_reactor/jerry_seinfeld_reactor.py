import os

from ailive.actions.plugins.readers.bbc_titles_reader import AliveBBCNewsPlugin
from ailive.actions.plugins.writers.wordpress import WordPressAlivePlugin
from ailive.engine.chatgpt.prompts.funny_prompts import jerry_seinfeld_prompt
from ailive.infra import log_config  # noqa: F401
from ailive.infra.base_entity import AiLive

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="FUNNY_NEWS",
    settings_files=['settings.yaml', '.secrets.yaml'],
)


class NewsReactor(AiLive):
    def get_plugins(self):
        plugins = []
        wp_config = settings.plugins.wordpress1
        wordpress_plugin = WordPressAlivePlugin(
            base_url=wp_config.base_url,
            username=wp_config.username,
            password=wp_config.password,
            tags=['funny', 'jerry seinfeld']
        )
        plugins.append(wordpress_plugin)
        news_plugin = AliveBBCNewsPlugin(
            scrape_recent_news=os.environ.get("SCRAPE_RECENT", False),
        )
        plugins.append(news_plugin)
        return plugins


def main():
    alive_bot = NewsReactor(prompt=jerry_seinfeld_prompt,
                            v_name="Jerry Seinfeld GPT",
                            sleep_seconds=10)
    alive_bot.run_forever()


if __name__ == '__main__':
    main()
