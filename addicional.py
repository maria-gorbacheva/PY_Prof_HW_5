import requests
from bs4 import BeautifulSoup
from _datetime import datetime

KEYWORDS = ['9000', 'магнитное', 'Аня']

ret = requests.get('https://habr.com/ru/all/')
soup = BeautifulSoup(ret.text, 'html.parser')

posts = soup.find_all('article', class_='post')

for post in posts:
    post_preview = post.find_all('div', class_='post__text')
    preview_texts = list(map(lambda t: t.text.strip().lower(), post_preview))

    for preview in preview_texts:
        preview_lower = preview.lower()
        link = post.find('a', class_='post__title_link')
        link_link = link.attrs.get('href')

        def print_row():
            dt = post.find('span', class_='post__time').text
            ddt = dt.replace('сегодня', f'{datetime.date(datetime.now())}')
            link_text = link.text.strip()
            print(ddt, link_text, link_link)

        if any([desired in preview_lower for desired in KEYWORDS]):
            print_row()
            break

        else:
            article_link = requests.get(link_link)
            article = BeautifulSoup(article_link.text, 'html.parser')
            content = article.find('div', class_='post__body')

            if any(desired in content.text.lower() for desired in KEYWORDS):
                print_row()
                break

