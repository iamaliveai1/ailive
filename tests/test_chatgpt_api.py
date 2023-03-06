from ailive.engine.chatgpt.chatgpt_api import ask_gpt_long_content
from ailive.engine.chatgpt.chatgpt_api import ask_gpt


def test_ask_gpt_long_content():
    print("Starting test_ask_gpt_long_content")
    print("#" * 50)
    result = ask_gpt_long_content(
        content=[
            "this is a test content, written without a style.",
            "hello world! how are you?"
        ],
        prompt="this is a test prompt"
    )
    assert result and len(result) > 0


def test_ask_gpt():
    print("Starting test_ask_gpt")
    print("#" * 50)
    result = ask_gpt(prompt="hello world! how are you?")
    assert result and len(result) > 0


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
