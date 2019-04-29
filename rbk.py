import requests
from lxml import html
import csv


headers = {'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
base_url = 'https://www.rbc.ru/'


def rbk_parser(base_url, headers):
    page = requests.get(base_url, headers=headers)
    three = html.fromstring(page.content)
    title = three.xpath('//span[@data-vr-headline=""]/text()')
    url = three.xpath('//a[@data-yandex-name="from_main"]/@data-vr-contentbox-url')
    publication_date = three.xpath('//div[@data-id]/@data-modif-date')
    news = []
    for i in range(len(title)):
        news.append({
            'url': url[i],
            'title': title[i],
            'publication_date': publication_date[i]
            })
    return news


def files_writer_csv(news):
    with open('parser_news.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('URL', 'Заголовок новости', 'Дата публикации'))
        for new in news:
            a_pen.writerow((new['url'], new['title'], new['publication_date']))


def files_writer_txt(news):
    with open('parser_news.txt', 'w') as file:
        for new in news:
            file.write(
                'URL:' + ' ' + str(new['url']) + '\n'
                'Заголовок новости:' + ' ' + str(new['title']) + '\n'
                'Дата публикации:' + ' ' + str(new['publication_date'] + '\n' + '\n')
                )


news = rbk_parser(base_url, headers)
files_writer_csv(news)
files_writer_txt(news)
