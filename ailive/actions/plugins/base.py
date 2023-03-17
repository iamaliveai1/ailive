"""
Define the abstract base class for all plugins.
"""

import abc


class AlivePlugin(metaclass=abc.ABCMeta):
    """
    Define the interface (and default implementation) for all plugins.
    """
    can_post = False
    can_comment = False
    can_like = False
    can_follow = False

    def get_notifications(self):
        return []

    def create_post(self, title, content, categories=None, tags=None):
        pass
