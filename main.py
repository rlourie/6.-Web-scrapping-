import bs4
import requests
import re


def get_title_data(article):
    # print(article)
    title = article.find('h2')
    title_data = title.text
    return title_data


def get_hub_data(article):
    hub_data = ''
    hubs = article.find_all('a', class_="tm-article-snippet__hubs-item-link")
    for hub in hubs:
        hub_data += hub.find("span").text + ' '
    return hub_data


def get_body_data(article):
    body_data = ''
    bodys = article.find_all("div", class_="article-formatted-body article-formatted-body_version-2")
    for body in bodys:
        bodys = body.find_all("p")
        for tag in bodys:
            body_data += tag.text + " "
    return body_data


def get_time(article):
    time = article.find("time").get("title")
    return time


def get_href(article):
    href = article.find("h2").find("a").get('href')
    href = 'https://habr.com' + href
    return href


def get_the_right(articles, KEYWORDS):
    counter = 0
    for article in articles:
        result_data = (
                get_title_data(article) + " " + get_hub_data(article) + " " + get_body_data(
            article)).lower().strip()
        for word in KEYWORDS:
            patern = ""
            patern += word
            if re.search(patern, result_data):
                counter += 1
                print(f'{get_time(article)} {get_title_data(article)} {get_href(article)}')
    print(f'Найдено {counter}')


HEADERS = {
    'Cookie': 'feature_streaming_comments=true; _ym_uid=1645048962634853152; _ym_d=1645048962; _ym_isad=2; '
              '_ga=GA1.2.1326318411.1645048962; _gid=GA1.2.1335107927.1645048962; fl=ru; hl=ru; '
              '__gads=ID=9a751927c8924d92:T=1645092324:S=ALNI_MbbpqCZMhdGzJ0KCvBoL6ca7vwtXw',
    'Host': 'habr.com',
    'Referer': 'https://github.com/netology-code/py-homeworks-advanced/tree/master/6.Web-scrapping',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36""'}
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'it']

response = requests.get("https://habr.com/ru/all/", headers=HEADERS)
response.raise_for_status()
text = response.text

soup = bs4.BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article', class_="tm-articles-list__item")
get_the_right(articles, KEYWORDS)
