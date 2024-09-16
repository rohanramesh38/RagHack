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
  'cookie': 'blab=820fb4ec-3aa4-4ca4-9c0a-970ef36e70c7; cleared-onetrust-cookies=; tglr_anon_id=a0b239d1-d766-40d0-b527-f0e0a764065d; tglr_hash_id=h_5c4c7d07579ba33dd717dc868dcb9464b34c51dd10d80400bdbe86e07e29abf4; tglr_http_only=a0b239d1-d766-40d0-b527-f0e0a764065d; tglr_tenant_id=src_1Tqf7BF96WTbG5QbUndHWIgKoFo; pmpdid=12352c1d-dc88-4aac-aa71-61737d3cd76a; OTGPPConsent=DBABLA~BVQqAAAACgA.QA; cohsn_xs_id=9323b38c-dc36-4e8a-8e8d-cffe0c4070e6; usprivacy=1YNY; _ga=GA1.1.1560048711.1725942301; _lr_geo_location_state=MI; _lr_geo_location=US; FPID=FPID2.2.0TEyroj1K6jhpEQHDov1Z%2BoMPohKYOggLHOb1kcf1w8%3D.1725942301; _fbp=fb.1.1725942307577.757530757641383141; _tt_enable_cookie=1; _ttp=zc8bsg6SaDae2UG2lb2ixqVa9tU; _pin_unauth=dWlkPVpEQTNPRGt4WVRVdE9USTROeTAwWmprd0xXRmhZMlF0T1RneU9ESTVZbVZpTVdFMA; dmd-tag=56a45d50-be44-11ee-a8c5-a327dc484fe9; _lr_env_src_ats=false; idl_env=At2XiNpVUEAd0jvooyDMBkauZwq6DLcDu05L4R9RAUEV_zREcylRo7x2jUk; idl_env_cst=xiyGLDQsMg%3D%3D; connectId=%7B%22puid%22%3A%22e9ca44f67ad59da62507e7fbac8ea74f12cafea09a397b6fc54091029c30dc80%22%2C%22vmuid%22%3A%22PI2JQo9h3JS-1YqnRCB86IIJ_fHJPfACPzDJfRsHId_xi34StReEhJPWbwjxnHEqcwNdI6-1sN2tdL2Lb9xQCw%22%2C%22connectid%22%3A%22PI2JQo9h3JS-1YqnRCB86IIJ_fHJPfACPzDJfRsHId_xi34StReEhJPWbwjxnHEqcwNdI6-1sN2tdL2Lb9xQCw%22%2C%22connectId%22%3A%22PI2JQo9h3JS-1YqnRCB86IIJ_fHJPfACPzDJfRsHId_xi34StReEhJPWbwjxnHEqcwNdI6-1sN2tdL2Lb9xQCw%22%2C%22ttl%22%3A86400000%2C%22he%22%3A%22%22%2C%22lastSynced%22%3A1725942316914%2C%22lastUsed%22%3A1725942316914%7D; _lr_sampling_rate=100; tglr_sess_id=f7a3b3d7-de86-4161-8a3c-dd1a3003bd4f; tglr_ref=; tglr_req=https://www.healthline.com/health/fitness/cycling-vs-walking; tglr_sess_count=2; tglr_smpl=0; FPLC=THbORf3rOA93UuQ5W6nkBkLBHDr9fUTigNzqTTH%2FA4dBFttnAgqP39dNdGIVbwmjC%2F21YpFV9LXXF%2BkdFPrO4gZhofJFyTWqx4L%2BSpLYHybqQ0uSbi0zJ5UtNoPZwg%3D%3D; dmd-sid4={%22id%22:%22c182c7c0-6fd7-11ef-ba0d-cbbe0f65b8ec%22%2C%22timestamp%22:1726015791000}; _clck=166wni0%7C2%7Cfp3%7C0%7C1714; _ga_0N29CNZT79=GS1.1.1726015698.2.1.1726017435.0.0.1286992122; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Sep+10+2024+21%3A17%3A15+GMT-0400+(Eastern+Daylight+Time)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5f94952f-7262-4c55-bb89-cc990716b549&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&GPPCookiesCount=1&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=US%3BMI; OptanonAlertBoxClosed=2024-09-11T01:17:15.236Z; chsn_cnsnt=www.healthline.com%3AC0001%2CC0002%2CC0003%2CC0004; _rdt_uuid=1725942307492.c8b93988-1251-45fe-885d-d01a864de867; sailthru_pageviews=4; _uetsid=a8fc96806f2c11efa0d84d085c401caf; _uetvid=a8fc99806f2c11ef8ac831145eb6e00e; sailthru_content=401c985ddf345bff6f1916c516fcc1d27f6a3ea345ec5398531336fe088d04f497aacedf0bb73ec16c903611668993b462032e0eb44d51c9887d80b4f3a07bfe; sailthru_visitor=19c914ec-76ca-4159-810e-b44f90a6a8e9; _clsk=1j3tv15%7C1726017443277%7C4%7C0%7Cp.clarity.ms%2Fcollect; __gads=ID=19a91ee02612fe4f:T=1725942318:RT=1726017443:S=ALNI_Mbwcpq_weq6sNlkgPNvK6GPdGtWcA; __eoi=ID=82e5184f9fd1c8a4:T=1725942318:RT=1726017443:S=AA-AfjZWekL-uiQ5EYttlTMr5Esl; blab=e0e9b771-2841-46c5-95ed-6c177e582f2a; lastContentSeen=/health/fitness/cycling-vs-walking|fitness',
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