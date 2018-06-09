# encoding=utf-8
import requests
from bs4 import BeautifulSoup
import math
import sys
from multiprocessing import Process
import os

"""
分析：
# 获取目录分类
http://www.ximalaya.com/revision/category/allCategoryInfo

#获取所有的album
http://www.ximalaya.com/revision/category/queryCategoryPageAlbums?category=youshengshu&subcategory=&meta=&sort=0&page=2&perPage=30


获取album的音频列表拿到trackId
http://www.ximalaya.com/revision/album?albumId=5258023

Referer: http://www.ximalaya.com/youshengshu/2854032/

拿到trackId后获取音频地址
http://www.ximalaya.com/revision/play/tracks?trackIds=8259821

Referer: http://www.ximalaya.com/waiyu/5258023/
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36


""" 
# 伪造allCategoryInfo请求头
catagory_header = {
'Cookie':'_xmLog=xm_1528372350671_ji4hfpanjstquv; _ga=GA1.2.105022450.1528372351; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1528440965,1528442411,1528443437,1528520885; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1528520885',
'Referer':'https://www.ximalaya.com/category/',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}
category_url = 'http://www.ximalaya.com/revision/category/allCategoryInfo'
category_dict = {}
# 获取目录名称以及link
def get_all_category():
    data = requests.get(category_url, headers=catagory_header).json()
    data = data['data']
    for categorie_list in data:
        categorys = categorie_list['categories']
        for category in categorys:
            category_dict[category['name']] = category['displayName']           
    return category_dict

    
# 获取目录下面所有的album
categoryPageAlbums_url = 'http://www.ximalaya.com/revision/category/queryCategoryPageAlbums'
categoryPageAlbums_header = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
'Cookie': '_xmLog=xm_1528372350671_ji4hfpanjstquv; _ga=GA1.2.105022450.1528372351; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1528440965,1528442411,1528443437,1528520885; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1528520885'
}
def get_category_all_albums(category_name):
    categoryPageAlbums_header['Referer'] = 'https://www.ximalaya.com/'+category_name+'/'
    params={}
    params['category'] = category_name
    params['subcategory'] = ''
    params['meta'] = ''
    params['sort'] = '0'
    params['page'] = '1'
    params['perPage'] = '30'
    data = requests.get(categoryPageAlbums_url, headers=categoryPageAlbums_header,params=params).json()
    data = data['data']
    total = data['total']
    albums = data['albums']
    albums_dict = {}
    for album in albums:
        albums_dict[album['albumId']] = album['title']
    # category_all_albums_dict[category_name] = albums_dict 
    pages = math.ceil(total/data['pageSize'])
    for i in range(1,pages):
        params['page'] = i+1
        data = requests.get(categoryPageAlbums_url, headers=categoryPageAlbums_header,params=params).json()
        data = data['data']
        albums = data['albums']
        for album in albums:
            albums_dict[str(album['albumId'])] = album['title']        
    return albums_dict
 
#获取音频url
track_ids=[]
def get_vedio_url(category_name,albumId):
    url = 'http://www.ximalaya.com/revision/album'
    header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Cookie':'_xmLog=xm_1528372350671_ji4hfpanjstquv; trackType=web; x_xmly_traffic=utm_source%3A%26utm_medium%3A%26utm_campaign%3A%26utm_content%3A%26utm_term%3A%26utm_from%3A; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1528372334,1528372351; _ga=GA1.2.105022450.1528372351; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1528378517'
    }
    header['Referer']='http://www.ximalaya.com/'+category_name+'/'+albumId+'/'
    params={}
    params['albumId']= albumId
    data = requests.get(url,headers=header,params=params).json()
    data = data['data']
    tracksInfo = data['tracksInfo']
    #获取总条数，并计算总页数
    pageCount = math.ceil(tracksInfo['trackTotalCount']/tracksInfo['pageSize'])
    for pageNum in range(pageCount):
        pageNum = pageNum+1
        url = 'http://www.ximalaya.com/revision/album/getTracksList'
        header['Referer']='http://www.ximalaya.com/youshengshu/2854032/p'+str(pageNum)+'/'
        params['pageNum'] = str(pageNum)
        data = requests.get(url,headers=header,params=params).json()
        data = data['data']
        tracks = data['tracks']
        for track in tracks:
            track_ids.append(track['trackId'])   
            
    header['Referer']='http://www.ximalaya.com/'+category_name+'/'+albumId+'/'
    header['Cookie']='_xmLog=xm_1528372350671_ji4hfpanjstquv; _ga=GA1.2.105022450.1528372351; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1528372334,1528372351,1528422022; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1528427460'
    track_url='http://www.ximalaya.com/revision/play/tracks'
    track_result = {}
    c = set(track_ids)
    param1={}
    for trackId in c:
        param1['trackIds']= str(trackId)
        try:
            content = requests.get(track_url,headers=header,params=param1).json()
            content = content['data']
            tracksForAudioPlay = content['tracksForAudioPlay']
            tarcks = tracksForAudioPlay[0]
            if(tarcks['src'] is not None and tarcks['trackName'] is not None):
                track_result[tarcks['trackName']]=tarcks['src']     
        except:
            continue
    return track_result
 
 #开进程去处理每个目录的音频
def process(category,categoryName):
    #创建一级目录
    dir = 'C://Users/GuiRunning/Desktop/python-learn/ximalaya-vedio/vedio/'+categoryName+'/'
    isExists=os.path.exists(dir)   
    if not isExists:
        os.makedirs(dir) 
    albums_dict=get_category_all_albums(category)
    for albumId,albumName in albums_dict.items():
        file = dir+albumName+'.txt'
        try:
            with open(file, 'a',encoding='utf-8') as fp:
                for trackName,url in get_vedio_url(category,albumId).items():
                    fp.write(trackName+'==>'+url+'\n')
        except:
            continue
            

def main():
    all_category = get_all_category()
    for k,v in all_category.items():
        process(k,v)
        p = Process(target=process, args=(v,))
        p.start()
        p.join()

if __name__ == '__main__':
    main()
