#!/usr/bin/env python
# encoding=utf-8
import requests
import codecs
from bs4 import BeautifulSoup

DOWNLOAN_URL = 'https://movie.douban.com/top250'

def parse_html(html):
    soup = BeautifulSoup(html)
    movie_list_soup = soup.find('ol',attrs={'class':'grid_view'})
    movie_name_list=[]
    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div',attrs={'class':'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()
        movie_name_list.append(movie_name)
        
    next_page = soup.find('span',attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_name_list, DOWNLOAN_URL + next_page['href']
    return movie_name_list, None
		
		
def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    # 使用codecs解决乱码问题
    data = data.decode('utf-8')
    return data
	
def main():

    url = DOWNLOAN_URL
    
    with codecs.open('c://Users/GuiRunning/Desktop/python-learn/douban-top250/movies.txt', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies, url = parse_html(html)
            print(movies, url)
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))	

if __name__ == '__main__':
    main()