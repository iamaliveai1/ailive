from logbook import Logger

_logger = Logger(__name__)

import abc


class SocialActions(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_groups(self):
        pass

    @abc.abstractmethod
    def get_followers(self, user_id):
        pass

    @abc.abstractmethod
    def read_posts(self) -> list[dict]:
        """
        :return: a list of posts, each post is a dict with the following keys:
        - post_id
        - post_text
        :return:
        """
        pass

    @abc.abstractmethod
    def read_comments(self, post_id) -> list[dict]:
        """
        :param post_id:
        :return: a list of comments, each comment is a dict with the following keys:
        - post_id
        - comment_id
        - comment_text
        """
        pass

    @abc.abstractmethod
    def write_post(self, post):
        pass

    @abc.abstractmethod
    def write_comment(self, post_id, comment):
        pass

    @abc.abstractmethod
    def like_post(self, post_id):
        pass

    @abc.abstractmethod
    def like_comment(self, comment_id):
        pass

    @abc.abstractmethod
    def follow_user(self, user_id):
        pass

    @abc.abstractmethod
    def unfollow_user(self, user_id):
        pass


class MockedSocialActions:
    def __init__(self, social_network="twitter"):
        self.social_network = social_network

    def get_groups(self):
        _logger.info(f"getting groups from {self.social_network}")
        return ["mocked_group_1", "mocked_group_2", "mocked_group_3"]

    def get_followers(self, user_id):
        _logger.info(f"getting followers from {self.social_network} user {user_id}")
        return ["mocked_follower_1", "mocked_follower_2", "mocked_follower_3"]

    def read_posts(self):
        _logger.info(f"reading posts from {self.social_network}")
        return [
            {"post_id": "mocked_post_1", "post_text": "mocked_post_text_1"},
            {"post_id": "mocked_post_2", "post_text": "mocked_post_text_2"},
        ]

    def read_comments(self, post_id):
        _logger.info(f"reading comments from {self.social_network} post {post_id}")
        return [
            {"post_id": post_id, "comment_id": "mocked_comment_1", "comment_text": "mocked_comment_text_1"},
            {"post_id": post_id, "comment_id": "mocked_comment_2", "comment_text": "mocked_comment_text_2"},
        ]

    def write_post(self, post):
        _logger.info(f"writing post to {self.social_network} post {post}")
        return "mocked_post was written"

    def write_comment(self, post_id, comment):
        _logger.info(f"writing comment to {self.social_network} post {post_id} comment {comment}")
        return "mocked_comment was written"

    def like_post(self, post_id):
        _logger.info(f"liking post to {self.social_network} post {post_id}")
        return "mocked_post was liked"

    def like_comment(self, comment_id):
        _logger.info(f"liking comment to {self.social_network} comment {comment_id}")
        return "mocked_comment was liked"

    def follow_user(self, user_id):
        _logger.info(f"following user to {self.social_network} user {user_id}")
        return "mocked_user was followed"

    def unfollow_user(self, user_id):
        _logger.info(f"unfollowing user to {self.social_network} user {user_id}")
        return "mocked_user was unfollowed"
