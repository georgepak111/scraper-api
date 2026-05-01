import sys
import json
import requests
from bs4 import BeautifulSoup

data = json.loads(sys.stdin.read())  # fixed the link issue
url = data["url"]

def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return None

def clean_html(html_string):  # now takes a string, not a filename
    soup = BeautifulSoup(html_string, "html.parser")
    body_text = soup.body.get_text(separator="\n", strip=True)
    return body_text

def main(url):
    html = get_html(url)
    if html is None:
        print("BAD REQUEST")
        return
    cleaned = clean_html(html)
    print(cleaned)

main(url)
