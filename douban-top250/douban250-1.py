#!/usr/bin/env python
# encoding=utf-8
import requests
import codecs
DOWNLOAN_URL = 'https://movie.douban.com/top250'


def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    # 使用codecs解决乱码问题
    data = data.decode('utf-8')
    return data
	
def main():
	print(download_page(DOWNLOAN_URL))

if __name__ == '__main__':
    main()