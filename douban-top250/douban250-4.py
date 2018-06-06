#!/usr/bin/env python
# encoding=utf-8
import requests
import codecs
from bs4 import BeautifulSoup

DOWNLOAN_URL = 'https://movie.douban.com/top250'
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}

def parse_html(html):
    soup = BeautifulSoup(html)
    img_list_soup = soup.find('ol',attrs={'class':'grid_view'})
    img_dict = {}
    for img_li in img_list_soup.find_all('li'):
        detail = img_li.find('div',attrs={'class':'pic'}).find('a')
        img_name = detail.find('img')['alt']
        img_url = detail.find('img')['src']
        img_dict[img_name] = img_url;
        
    next_page = soup.find('span',attrs={'class': 'next'}).find('a')
    if next_page:
        return img_dict, DOWNLOAN_URL + next_page['href']
    return img_dict, None
		
	
def download_page(url):
    data = requests.get(url, headers=HEADER).content
    # 使用codecs解决乱码问题
    data = data.decode('utf-8')
    return data
	
def main():
    url = DOWNLOAN_URL
    while url:
        html = download_page(url)
        imgs, url = parse_html(html)
        print(imgs, url)
        for key in imgs.keys():
            print(imgs[key])
            with open('c://Users/GuiRunning/Desktop/python-learn/douban-top250/images/%s.jpg' % (key), 'wb') as fp:
                data = requests.get(imgs[key], headers=HEADER).content
                fp.write(data)

if __name__ == '__main__':
    main()