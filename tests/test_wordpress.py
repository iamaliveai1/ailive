from time import sleep

from ailive.actions.plugins.writers.wordpress import WordPressAlivePlugin
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

