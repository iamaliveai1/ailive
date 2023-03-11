import requests
from bs4 import BeautifulSoup
from readability import Document


def write_to_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content)


def add_headers_to_html(html: str) -> str:
    """
    This function adds headers to the html
    :param html: the HTML string to add headers to
    :param headers: the headers to add, as a string
    :return: the updated HTML string with headers
    """
    soup = BeautifulSoup(html, "html.parser")

    # create a new <head> tag
    new_head = soup.new_tag("head")

    # create the <meta> tags from the headers string
    meta_charset = soup.new_tag("meta", charset="UTF-8")

    # append the <meta> tags to the new_head tag
    new_head.append(meta_charset)

    # insert the new <head> tag at the beginning of the document
    soup.html.insert(0, new_head)

    return str(soup)


def get_clean_html(url):
    response = requests.get(url)
    doc = Document(response.content)
    print("Parsing document...")
    print(f"title: {doc.title()}")
    print(f"summary:\n{len(doc.summary())}")
    clean_html = doc.summary()

    final_html = add_headers_to_html(clean_html)
    return final_html


def download_clean_html(url, filename='readability_1.html'):
    final_html = get_clean_html(url)
    write_to_file(final_html, filename)


def main():
    url = 'https://brasilcasinos.com.br/crash-aposta/aviator/'
    download_clean_html(url)


if __name__ == '__main__':
    main()
