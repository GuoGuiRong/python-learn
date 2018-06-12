# encoding=utf-8
import requests
from bs4 import BeautifulSoup
import math
import sys
import time
from multiprocessing import Pool
import os
import hmac
import hashlib

"""
多进程的使用
""" 
def do_encode(key,url):
    md5 = hashlib.md5()
    h = hmac.new(key.encode('utf-8'), url.encode('utf-8'), digestmod='MD5')
    print('进程'+str(os.getpid())+'完成加密'+h.hexdigest())
    

def main():
    p=Pool(2)  #定义2个进程池
    urls = ['http://fdfs.xmcdn.com/group42/M04/A3/66/wKgJ81q0u22CDqmDAB3gb50LCrs820.mp3','http://fdfs.xmcdn.com/group41/M07/04/89/wKgJ8VrIwlGivmWZAAoLs1DnVUI131.mp3','http://fdfs.xmcdn.com/group42/M0A/AD/ED/wKgJ9FrEXz7SAvXUABhFVUKgrJQ522.mp3']
    for url in urls:
        p.apply_async(func=do_encode,args=('ggr',url,)) #异步执行任务
        
    p.close()
    p.join()

if __name__ == '__main__':
    main()