import requests
from bs4 import BeautifulSoup

# Make a GET request to the CNN homepage
response = requests.get('https://edition.cnn.com/')
# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the title elements on the page
titles = soup.find_all('h3')

# Loop through each title element and extract the title text and link
for title in titles:
    title_text = title.get_text().strip()
    title_link = title.find('a')['href']
    print(title_text)
    print(title_link)
