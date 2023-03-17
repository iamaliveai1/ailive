from time import sleep

from ailive.actions.plugins.writers.wordpress import WordPressAlivePlugin, get_gpt_categories, get_gpt_tags
from ailive.config import settings


def test_wordpress_publish():
    content = "<h1>hello world 2 </h1>"
    title = "hello world 3"
    wp_config = settings.plugins.wordpress1
    wordpress_plugin = WordPressAlivePlugin(
        base_url=wp_config.base_url,
        username=wp_config.username,
        password=wp_config.password,
    )
    response = wordpress_plugin.create_post(
        title=title,
        content=content)
    response.raise_for_status()
    assert response.status_code == 201
    result = response.json()
    print(f'website link: {result["guid"]["rendered"]}')
    sleep(10)
    deletion_response = wordpress_plugin.delete_page(result["id"])
    assert deletion_response.status_code == 200


# unittest for get_gpt_categories
# Path: AiLive/ailive/tests/test_wordpress.py
def test_get_gpt_categories():
    content = """
    What's the deal with soccer teams and "end of an era" talk? I mean, Liverpool gets crushed by Real Madrid and suddenly, it's doom and gloom for Jurgen Klopp's side! It's like when you lose one game of Monopoly and everyone thinks you're bankrupt!
    
    And let's talk about the Champions League. It's like the VIP club of soccer. One minute you're in, the next you're out, and then you're trying to sneak back in with a fake mustache and glasses. "Hey, remember us? We won in 2019!"
    
    But seriously, folks, Klopp says it's a "massive task" to get back in the Champions League. It's like trying to find a parking spot in Manhattan on a Saturday night. Good luck with that!
    """
    categories = get_gpt_categories(content)
    assert categories
    assert len(categories) > 5


def test_get_gpt_tags():
    content = """
    What's the deal with soccer teams and "end of an era" talk? I mean, Liverpool gets crushed by Real Madrid and suddenly, it's doom and gloom for Jurgen Klopp's side! It's like when you lose one game of Monopoly and everyone thinks you're bankrupt!
    
    And let's talk about the Champions League. It's like the VIP club of soccer. One minute you're in, the next you're out, and then you're trying to sneak back in with a fake mustache and glasses. "Hey, remember us? We won in 2019!"
    
    But seriously, folks, Klopp says it's a "massive task" to get back in the Champions League. It's like trying to find a parking spot in Manhattan on a Saturday night. Good luck with that!
    """
    tags = get_gpt_tags(content)
    assert tags
    assert len(tags) > 5
