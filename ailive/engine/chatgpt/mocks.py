def get_mock_chatbot():
    # return MockChatbot()
    return MockChatbot()


class MockChatbot:
    conversation_id = 0
    parent_id = 0

    def __init__(self):
        pass

    def ask(self, prompt):
        """
        This method mocks the Chatbot.ask method and returns a mocked answer as follows:
        [
        {"message": "mocked answer"},
        {"message": "mocked answer"},
        ]
        :param prompt:
        :return:
        """
        return [
            {"message": prompt, "conversation_id": self.conversation_id, "parent_id": self.parent_id},
        ]

    def delete_conversation(self, conversation_id):
        pass

    def reset_chat(self):
        pass


class MockSocialChatbot:
    conversation_id = 0
    parent_id = 0

    def __init__(self):
        pass

    def ask(self, prompt):
        """
        This method mocks the Chatbot.ask method and returns a mocked answer as follows:
        [
        {"message": "mocked answer"},
        {"message": "mocked answer"},
        ]
        :param prompt:
        :return:
        """
        possible_actions = [
            "like_post('post_id')",
            'write_comment(photo_id, "Thank you for tagging me in this photo")'
        ]
        return [
            {"message": action, "conversation_id": self.conversation_id, "parent_id": self.parent_id}
            for action in possible_actions
        ]

    def delete_conversation(self, conversation_id):
        pass

    def reset_chat(self):
        pass
