import requests
from bs4 import BeautifulSoup

def get_bbc_sports_titles():
    # Define the URL of the BBC sports page
    url = 'https://www.bbc.com/sport'

    # Send a GET request to the URL and store the response in a variable
    response = requests.get(url)

    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the sports titles on the page and store them in a list
    sports_titles = []
    for article in soup.find_all('div', {'type': 'article'}):
        title = article.find('h3', class_='gs-c-promo-heading__title gel-paragon-bold nw-o-link-split__text')
        if title:
            sports_titles.append(title.text)

    # Return the list of sports titles
    return sports_titles


if __name__ == '__main__':
    get_bbc_sports_titles()