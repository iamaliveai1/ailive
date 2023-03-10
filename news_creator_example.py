"""
This is an example of how to use the chatbot to create news articles.
It uses the BBC news website to get the latest news headlines, and then uses the chatbot to generate a news article for each headline.
It then uses the chatbot to format the article, and finally publishes it to a WordPress blog.
"""
import json

import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth


from revChatGPT.V1 import Chatbot
chat_gpt = Chatbot(config={
    "email": "email",
    "password": "password"
})


def get_news():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    # create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all the news article titles on the page
    titles = soup.find_all('h3', class_='gs-c-promo-heading__title')

    # print out the titles
    for title in titles:
        print(title.get_text())

    return [title.get_text() for title in titles]


def react_to_news(html_formatter_prompt, prompt, url):
    news = get_news()
    for title in news:
        gpt_opinions = ask_gpt(prompt + title)
        formatted_content = ask_gpt(html_formatter_prompt + gpt_opinions)
        publish_to_wordpress(formatted_content, title, url)


def ask_gpt(prompt):
    gpt_response = chat_gpt.ask(prompt)
    result = list(gpt_response)
    answer = result[-1]["message"]
    return answer


def publish_to_wordpress(formatted_content, title, url):
    payload = json.dumps({
        "status": "publish",
        "title": title,
        "content": formatted_content,
    })
    auth = HTTPBasicAuth("username", "password")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    requests.post(url, data=payload, headers=headers, auth=auth)


def main():
    # https://github.com/f/awesome-chatgpt-prompts#act-as-a-commentariat
    prompt = (
        "I want you to act as a commentariat. "
        "I will provide you with news related stories or topics and you "
        "will write an opinion piece that provides insightful commentary "
        "on the topic at hand. "
        "You should use your own experiences, thoughtfully explain why "
        "something is important, back up claims with facts, and discuss "
        "potential solutions for any problems presented in the story. "
        "My first request is :"
    )

    html_formatter_prompt = (
        "Write the following as HTML document, with nice tags and headings etc. "
        "place <div>, <p>, <br>, <a>, <h1>, <h2>, <h3> etc where you think it is best. "
        "Text:"
    )
    domain = "https://domain.com"
    url = f"{domain}/wp-json/wp/v2/posts"

    # run main logic
    react_to_news(html_formatter_prompt, prompt, url)

