import sys
import json
import requests
from ai_api import analyse
from bs4 import BeautifulSoup

def log(msg):
    print(msg, file=sys.stderr, flush=True)  # logs to Node's stderr

data = json.loads(sys.stdin.read())
url = data["url"]
log(f"Received URL: {url}")

def get_html(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
        }
        response = requests.get(url, headers=headers, timeout=10)
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
