#!/usr/bin/env python
# encoding=utf-8
import requests
import codecs
DOWNLOAN_URL = 'https://movie.douban.com/top250'

'''
使用codecs是为了方便处理中文编码
使用请求中带入header 是为了更加真实模拟浏览器请求，同时避开最基本的反爬虫检验（U-A校验）
'''
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