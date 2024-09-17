import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import pdfkit
import html2text

import markdownify 
import markdown
import pdfkit



import requests

url = "https://www.healthline.com/health/fitness/cycling-vs-walking"

payload = {}
headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'cache-control': 'max-age=0',
  'priority': 'u=0, i',
  'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}


def get_soup(url):
    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_all_articles(soup):
    article = soup.find('div', class_="css-14cfce3")
    return article

soup = get_soup(url)
article = f"{get_all_articles(soup)}"

h = markdownify.markdownify(article, heading_style="ATX") 
with open('article.md', 'w') as file:
    file.write(h)

pdfkit.from_file('article.md', 'article.pdf')
