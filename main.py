import requests
from bs4 import BeautifulSoup
from _datetime import datetime

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'бэкенд']

ret = requests.get('https://habr.com/ru/all/')
soup = BeautifulSoup(ret.text, 'html.parser')

# извлекаем посты
posts = soup.find_all('article', class_='post')

for post in posts:
    post_preview = post.find_all('div', class_='post__text')
    preview_texts = list(map(lambda t: t.text.strip(), post_preview))
    if not post_preview:
        continue

    for preview in preview_texts:
        preview_lower = preview.lower()

        if any([desired in preview_lower for desired in KEYWORDS]):
            dt = post.find('span', class_='post__time').text
            ddt = dt.replace('сегодня', f'{datetime.date(datetime.now())}')
            link = post.find('a', class_='post__title_link')
            link_link = link.attrs.get('href')
            link_text = link.text.strip()
            print(ddt, link_text, link_link)
            break
