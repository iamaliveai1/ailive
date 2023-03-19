"""
This module encapsulate reverse ChatGPT API, and adds:
- a mock mode, for testing
- a method to send long content to the API, by splitting it to smaller chunks
- rate limiting (sleeping) between requests
- error handling
"""
import os
import re
import time
from http import HTTPStatus

import logbook

from ailive.config import settings
from ailive.engine.chatgpt.mocks import get_mock_chatbot
from ailive.infra import log_config  # noqa: F401
from revChatGPT.V1 import ErrorType
from revChatGPT.typing import Error

_logger = logbook.Logger(__name__)

chatgpt_cfg = settings.chatgpt
email = chatgpt_cfg.email
password = chatgpt_cfg.password

mock = bool(os.environ.get("MOCK_GPT", False))

if mock is False and (not email or not password):
    raise Exception("GPT_EMAIL and GPT_PASSWORD must be set!"
                    "Place them in settings.yaml or set them as environment variables")


def get_new_chatbot(version=None, min_time_between_requests=60):
    if mock:
        return get_mock_chatbot()
    print(f"Creating new chatbot... (version: {version})")
    if version is None:
        version = chatgpt_cfg.version
    if version == "v1":
        from revChatGPT.V1 import Chatbot
        chatbot = Chatbot(config={
            "access_token": chatgpt_cfg.access_token,
        })
    elif version == "v3":
        from revChatGPT.V3 import Chatbot
        chatbot = Chatbot(
            api_key=chatgpt_cfg.api_key,
            system_prompt="",
        )
    elif version == "v4":
        from revChatGPT.V1 import Chatbot
        chatbot = Chatbot(config={
            "access_token": chatgpt_cfg.access_token,
            "model": "gpt-4"
        })
    else:
        raise Exception(f"Unknown chatgpt version: {chatgpt_cfg.version}")
    chatbot.min_time_between_requests = min_time_between_requests
    chatbot.last_request_time = time.time() - min_time_between_requests
    return chatbot


class RotatingChatbot:
    """
    This class is a wrapper for the Chatbot class, which rotates the chatbot when it encounters an error.
    """

    def __init__(self):
        try:
            self.chatbot = get_new_chatbot()
        except Exception as e:
            # print the exception and the stack trace
            _logger.info("Failed to create chatbot")
            raise e

    def rotate_chatbot(self):
        _logger.info("Rotating chatbot")
        self.chatbot = get_new_chatbot()


chatbot_wrapper = RotatingChatbot()


def get_chatbot():
    return chatbot_wrapper.chatbot


def ask_gpt_long_content(content: list, prompt, delete_conversation=True):
    """
    :param content: a list of strings, expected to be paragraphs of text
    :param prompt:
    :param delete_conversation:
    :return:
    """
    result = _ask_gpt_long_content(prompt, content)
    if delete_conversation:
        chatbot = chatbot_wrapper.chatbot
        conversation_id = chatbot.conversation_id
        chatbot.delete_conversation(conversation_id)
        chatbot.reset_chat()
        _logger.info(f"conversation {conversation_id} deleted")
    return result


def _ask_gpt_long_content(prompt, content, max_request_size=1500):
    total_length = sum([len(s) for s in content])
    _logger.info(f"total content length {total_length} and max_request_size {max_request_size}")
    _logger.info("expecting " + str(total_length / max_request_size) + " requests")
    result = []
    for group_string in _get_next_group(content, max_request_size):
        result.append(ask_gpt(prompt + group_string))
    return result


def _get_next_group(content: list[str], max_request_size: int):
    """
    this method groups strings from `content` such that the total result will be less than max_request_size
    :param content:
    :param max_request_size:
    :return:
    """
    i = 0
    while i < len(content):
        group = []
        while i < len(content):
            group.append(content[i])
            partial_content = "\n".join(group)
            if len(partial_content) > max_request_size:
                if len(group) == 1:
                    raise ValueError(f"len(group_string)={len(partial_content)} > max_request_size={max_request_size}")
                group.pop()
                break
            i += 1
        # in case last group is too long, split it to slices of up to max_request_size
        partial_content = "\n".join(group)
        clean_partial_content = partial_content.replace(";", " ")
        if len(partial_content) > max_request_size:
            _logger.info(
                f"len(group_string)={len(partial_content)} > request_size={max_request_size}, slicing to {max_request_size}")
            # return N slices (by period) of the partial content, each slice is up max_request_size.
            yield from _slice_partial_content(partial_content, max_request_size)
        yield clean_partial_content


def _slice_partial_content(content, max_request_size):
    """
    this method slices partial_content to slices of up to max_request_size, split by , or ;
    :param content:
    :param max_request_size:
    :return:
    """
    # split by period
    sentences = re.split("[.;]", content)
    # join slices until the length is less than max_request_size
    paragraph = ""
    for pc in sentences:
        if len(paragraph) + len(pc) < max_request_size:
            paragraph += pc + "."
        else:
            yield paragraph
            paragraph = pc + "."
    if paragraph:
        yield paragraph


def ask_gpt(prompt, chatbot=None, attempts=2, cleanup=False):
    _logger.info(f"===================\n")
    _logger.info(f"Asking GPT:\n{prompt}")
    try:
        if chatbot is None:
            chatbot = chatbot_wrapper.chatbot
        _wait_on_rate_limit(chatbot)
        if prompt == "":
            _logger.error("ask_gpt: prompt is empty")
            return ""
        response = chatbot.ask(prompt=prompt)
        # import ipdb; ipdb.set_trace()
        result = list(response)
        if not result:
            raise Error(
                source="ask",
                message="Empty response from GPT",
                code=ErrorType.EMPTY_RESPONSE
            )
        if chatgpt_cfg.version == "v1":
            answer = result[-1]["message"]
        elif chatgpt_cfg.version == "v3":
            answer = "".join(result)
        else:
            raise Exception(f"Unknown chatgpt version: {chatgpt_cfg.version}")
        _logger.info(
            f"prompt: {prompt[:100]}...\n"
            f"-------------------\n"
            f"content len: {len(prompt)}\n"
            f"answer len: {len(answer)}\n"
            f"answer: {answer}...\n"
            f"===================")
        if cleanup and hasattr(chatbot, "conversation_id"):
            # cleanup the conversation, allowing following methods to start a new conversation
            _logger.info(f"deleting conversation {chatbot_wrapper.chatbot.conversation_id}...")
            chatbot_wrapper.chatbot.delete_conversation(chatbot_wrapper.chatbot.conversation_id)
            chatbot_wrapper.chatbot.reset_chat()
        return answer
    except Error as e:
        retry = False
        if e.code == ErrorType.RATE_LIMIT_ERROR:
            _logger.info(f"ERROR: {e}")
            _logger.info(f"GPT-RATE-LIMIT-ERROR: waiting 1 hour before retrying")
            time.sleep(60 * 60)
            retry = True
        elif e.code in [ErrorType.SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR]:
            _logger.info(f"ERROR: {e}")
            _logger.info(f"GPT-SERVER-ERROR: waiting 1 minute before retrying")
            time.sleep(60)
            retry = True
        elif e.code in [ErrorType.EXPIRED_ACCESS_TOKEN_ERROR, ErrorType.INVALID_ACCESS_TOKEN_ERROR]:
            _logger.info(f"ERROR: {e}")
            _logger.info(f"creating new chatbot")
            chatbot_wrapper.rotate_chatbot()
            retry = True
        # elif e.code == ErrorType.EMPTY_RESPONSE:
        #     _logger.info(f"ERROR: {e}")
        #     _logger.info(f"empty response from GPT")
        #     return ""
        if retry and attempts > 0:
            _logger.info(f"retrying ask_gpt, attempts={attempts}")
            return ask_gpt(prompt, attempts=attempts - 1)
        _logger.info(f"ERROR: error_code={e.code}, error_message={e.message}")
        raise e


def _wait_on_rate_limit(chatbot):
    """
    This method waits for min_time_between_requests seconds between requests to the ChatGPT API
    :param min_time_between_requests:
    :return:
    """
    if mock:
        return
    min_time_between_requests = chatbot.min_time_between_requests
    assert hasattr(chatbot, "last_request_time")

    last_request_time = chatbot.last_request_time
    if last_request_time is not None:
        time_since_last_request = time.time() - last_request_time
        wait_time = min_time_between_requests - time_since_last_request
        if wait_time > 0:
            _logger.info(f"GPT-RATE-LIMIT: waiting {wait_time} seconds")
            time.sleep(wait_time)
            _logger.info(f"GPT-RATE-LIMIT: done waiting")
    chatbot.last_request_time = time.time()


def delete_previos_conversations():
    import time
    chatbot = get_chatbot()
    conversations = chatbot.get_conversations()
    for conversation in conversations:
        if conversation['title'] == 'New chat':
            chatbot.delete_conversation(conversation['id'])
            print(f"Deleted conversation {conversation['id']} - {conversation['title']}")
            waiting_time = 2  # Wait for 1 second before proceeding to the next conversation
            print(f"Waiting for {waiting_time} second(s)...")
            time.sleep(waiting_time)
