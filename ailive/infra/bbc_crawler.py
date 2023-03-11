import requests
from bs4 import BeautifulSoup
from readability import Document

from ailive.infra.readability_extractor import get_clean_html
from digi_ai.extractors.soup_extractor import extract_content_from_html

host = "https://www.bbc.com"
url = f"{host}/news"

# Fetch the website's HTML content
response = requests.get(url)
content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Find all the article titles and their links
titles = soup.find_all('h3', class_='gs-c-promo-heading__title')
links = soup.find_all('a', class_='gs-c-promo-heading')
links_contents = []

# Print the titles and links
for i in range(len(titles)):
    print("#" * 50)
    print(titles[i].text)
    rel_path = links[i]['href']
    page_url = host + rel_path
    print(page_url)
    response = requests.get(page_url)
    clean_content = extract_content_from_html(response.content, minimum_words_in_line=10)
    # doc = Document(response.content)
    # clean_content = doc.summary()
    print(clean_content[:10])
    content_string = " ".join(clean_content)
    print(f"content_string length: {len(content_string)}")
    links_contents.append(content)
    break
