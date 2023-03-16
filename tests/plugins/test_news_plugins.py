"""
this is a unittest for news plugins, using pytest framework
"""


import os
import sys

import pytest

from ailive.actions.plugins.readers.bbc_titles_reader import AliveBBCNewsPlugin, AliveBBCSportsPlugin


@pytest.fixture
def news_plugin():
    return AliveBBCNewsPlugin(scrape_recent_news=True)


@pytest.fixture
def sports_plugin():
    return AliveBBCSportsPlugin(scrape_recent_news=True)


def test_news_plugin(news_plugin):
    assert news_plugin.can_post is False
    notifictions = news_plugin.pull_titles()
    assert len(notifictions) > 0


def test_sports_plugin(sports_plugin):
    assert sports_plugin.can_post is False
    notifictions = sports_plugin.pull_titles()
    assert len(notifictions) > 0
    for n in notifictions:
        print(n)
