import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://reliefweb.int/disasters?advanced-search=%28TY4611%29"

headers={}
payload = {}
def get_soup(url):
    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_all_links_in_page(soup):
    h3_tags = soup.find_all('h3', class_='rw-river-article__title')
    links = [ (h3_tag.find('a').text ,h3_tag.find('a')['href']) for h3_tag in h3_tags]
    return links

def get_content_div(soup):
    content_text=''
    content_div = soup.find('div', class_='rw-entity-text__content')
    if content_div:
        content_text = content_div.get_text(strip=True)
    return content_text

def get_and_save_data(index, url):
    soup = get_soup(url)
    filename = f"disasters{index}.csv"

    links = get_all_links_in_page(soup)

    data = []
    for disaster, url in links:
        soup = get_soup(url)
        description = get_content_div(soup)
        data.append([disaster, description, url])

    df = pd.DataFrame(data, columns=["disaster", "description", "url"])
    df.to_csv(filename, index=False)

page=31
for i in range(0,page):
    if(i==0):
        url = f"https://reliefweb.int/disasters?advanced-search=%28TY4611%29"
    else:
        url = f"https://reliefweb.int/disasters?advanced-search=%28TY4611%29&page={i}"

    get_and_save_data(i,url)










