import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://tgstat.ru/tag/spb'
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
           "accept" :"*/*"}
FILE = 'cars.csv'

def get_html(url, params = None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", class_="card")

    cars = []

    for item in items:
        cars.append({
            'title': item.find('div', class_='font-16').get_text(),
            'about': item.find('div', class_='font-14').get_text(strip=True),
            'last': item.find('div', class_='text-center').get_text(strip=True),
            'link': item.find('a', class_='text-body').get('href')
        })
    return cars

def save_file(items, path):
    with open(path, "w", encoding="windows-1251", errors='ignore', newline = '') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Title', 'About', 'Last post', 'Link'])
        for item in items:
            writer.writerow([item['title'], item ['about'], item ['last'], item ['link']])


def parse():
    URL = input('Введите страницу tgstat: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        html = get_html(URL)
        cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f'{len(cars)} телеграм-каналов сохранено.')
        os.startfile(FILE)
    else:
        print('Error')

parse()
