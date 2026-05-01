import sys
import json
import requests
from ai-api import analyse
from bs4 import BeautifulSoup

def log(msg):
    print(msg, file=sys.stderr, flush=True)  # logs to Node's stderr

data = json.loads(sys.stdin.read())
url = data["url"]
log(f"Received URL: {url}")

def get_html(url):
    try:
        log(f"Fetching: {url}")
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        log(f"Status code: {response.status_code}")
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        log(f"Request failed: {e}")
        return None

def clean_html(html_string):
    try:
        soup = BeautifulSoup(html_string, "html.parser")
        body_text = soup.body.get_text(separator="\n", strip=True)
        return body_text
    except Exception as e:
        log(f"Parsing failed: {e}")
        return None

def main(url):
    html = get_html(url)
    if html is None:
        print("BAD REQUEST")
        return
    cleaned = clean_html(html)
    if cleaned is None:
        print("PARSE ERROR")
        return
    log("Success!")

    analysed = analyse(cleaned)
    if analysed is None:
        print("Analysis failed")
        return

    print(analysed)

main(url)
