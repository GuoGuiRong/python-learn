# encoding=utf-8
import requests
from bs4 import BeautifulSoup
import math
import sys
import os
import threading
from concurrent.futures import ThreadPoolExecutor
"""
使用线程池下载多个mp3音频文件，多线程适合IO操作，但是线程个数也是要合理才能实现最大的效率
"""
def download_mp3(url):
    print(threading.current_thread().name+'下载'+url+'开始...')
    header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Cookie': '_xmLog=xm_1528372350671_ji4hfpanjstquv; _ga=GA1.2.105022450.1528372351; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1528440965,1528442411,1528443437,1528520885; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1528520885'
    }
    data = requests.get(url,headers=header).content
    basePath = 'C://Users/GuiRunning/Desktop/python-learn/ximalaya-vedio/ximalaya-threadpool/'
    fileName = url.split('/')[-1]
    print(fileName)
    with open(basePath+fileName,'wb') as f:
        f.write(data)
    return url+'下载完成..'
     
     
def final_callback(future,*args,**kwargs):
    result = future.result()
    print(result)
    
pool = ThreadPoolExecutor(3)
def main():
    urls = ['http://fdfs.xmcdn.com/group42/M04/A3/66/wKgJ81q0u22CDqmDAB3gb50LCrs820.mp3','http://fdfs.xmcdn.com/group41/M07/04/89/wKgJ8VrIwlGivmWZAAoLs1DnVUI131.mp3','http://fdfs.xmcdn.com/group42/M0A/AD/ED/wKgJ9FrEXz7SAvXUABhFVUKgrJQ522.mp3']
    for url in urls:
        done = pool.submit(download_mp3,url)
        done.add_done_callback(final_callback)
      
if __name__ == '__main__':
    main()
    pool.shutdown(wait=True)
