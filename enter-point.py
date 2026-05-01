import sys
import json
import requests
from bs4 import BeautifulSoup

data = json.loads(sys.stdin.read())  # Read and parse the data from Node
url = data["url"]


def clean_html(filename):
    file = open(filename, "r")
    soup = BeautifulSoup(file, "html.parser")
    body_text = soup.body.get_text(separator="\n", strip=True)
    return(body_text)

def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        return html
    except requests.exceptions.RequestException:
        return "BAD REQUEST"

def main(url):
  all_html = get_html(url)
  cleaned = clean_html(all_html)
  print(cleaned)


main(url)
