import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


url = "https://reliefweb.int/disasters?advanced-search=%28TY4611%29"

headers={}
payload = {}
def get_soup(url):
    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_all_articles(soup):
    articles = soup.find_all('article', class_="rw-river-article--card rw-river-article rw-river-article--disaster")

    article_links = []


    for article in articles:
        header = article.find('header', class_='rw-river-article__header')
        footer = article.find('footer', class_='rw-river-article__footer')
        disaster=month=year=None
        if header:
            h3_tag = header.find('h3', class_='rw-river-article__title')
            if h3_tag and h3_tag.find('a'):
                link = h3_tag.find('a')['href']
                disaster=h3_tag.find('a').text

                disaster_name=disaster

                match = re.search(r'- (\w+) (\d{4})', disaster)
                if match:
                    month = match.group(1)
                    year = match.group(2)

                    disaster_name=disaster_name.replace(f'- {month} {year}','')


                status = disaster_type = affected_country = None
                if footer:
                    status_tag = footer.find('dd', class_='rw-entity-meta__tag-value--status--ongoing') or footer.find('dd', class_='rw-entity-meta__tag-value--status--past')
                    if status_tag:
                        status = status_tag.get_text(strip=True)
                    
                    disaster_type_tag = footer.find('dd', class_='rw-entity-meta__tag-value--disaster-type')
                    if disaster_type_tag:
                        disaster_type = disaster_type_tag.get_text(strip=True)
                    
                    affected_country_tag = footer.find('dd', class_='rw-entity-meta__tag-value--country')
                    if affected_country_tag:
                        affected_country = affected_country_tag.get_text(strip=True)

                article_links.append(( disaster_name,month,year,status, disaster_type, affected_country,link))


    return article_links
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
    filename = f"../data/new/disasters{index}.csv"

    links = get_all_links_in_page(soup)

    articles= get_all_articles(soup)

    #print(len(  articles), len(links),articles[0])

    data = []
    for disaster_name,month,year,status, disaster_type, affected_country,url in articles:
        soup = get_soup(url)
        description = get_content_div(soup)
        data.append([disaster_name, month,year,status,disaster_type,affected_country,description, url])

    df = pd.DataFrame(data, columns=["disaster", "month","year" , "status","disaster_type","affected_country","description", "reference"])
    df.to_csv(filename, index=False)

page=31
for i in range(0,page):
    if(i==0):
        url = f"https://reliefweb.int/disasters?advanced-search=%28TY4611%29"
    else:
        url = f"https://reliefweb.int/disasters?advanced-search=%28TY4611%29&page={i}"

    get_and_save_data(i,url)










