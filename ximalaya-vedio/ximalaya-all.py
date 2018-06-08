import requests
from bs4 import BeautifulSoup
import math
import sys  
import time

FIRST_URL = 'http://www.ximalaya.com/category/'
BASE_URL = 'http://www.ximalaya.com'
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Cookie':'_xmLog=xm_1528372350671_ji4hfpanjstquv; trackType=web; x_xmly_traffic=utm_source%3A%26utm_medium%3A%26utm_campaign%3A%26utm_content%3A%26utm_term%3A%26utm_from%3A; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1528372334,1528372351; _ga=GA1.2.105022450.1528372351; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1528372547',
    'If-None-Match': 'W/"28251-CSZM/tu6xVMcaPus+e+1NjCyXrI',
    'Upgrade-Insecure-Requests':'1'
    }

category_list={}
# 解析获取所有分类
def parse_category(url):
    data = requests.get(url, headers=HEADER).content
    # 使用codecs解决乱码问题
    data = data.decode('utf-8')
    soup = BeautifulSoup(data)
    category_hotword = soup.find('div',attrs={'class': 'e-2880429693 category_hotword'})
    plates = soup.find('div',attrs={'class': 'e-2880429693 plates'})
    category_hotword_dict={}
    category_hotword_plats={}
    
   
   # 解析热门分类 
    for category_hotword_wrapper in category_hotword.find_all('section',attrs={'class': 'e-2880429693 category_hotword-wrapper'}):
        hotword = category_hotword_wrapper.find('div',attrs={'class':'e-2880429693 hotword'})
        link_url = hotword.find('a')['href']
        link_name = hotword.find('img')['alt']
        category_hotword_dict[link_name] = BASE_URL+link_url
     

   # 解析其他分类        
    for plate in plates.find_all('div',attrs={'class': 'e-2880429693 category_plate'}):
        anchor = plate.find('div',attrs={'class': 'e-2880429693 anchor'})['id']#获取一级目录名称  
        body = plate.find('div',attrs={'class': 'e-2880429693 body'})
        subject_dict = {}
        
        for subject_wrapper in body.find_all('section',attrs={'class': 'e-2880429693 subject_wrapper'}):   
           c2 = subject_wrapper.find('div',attrs={'class':'e-2880429693 subject'}).find('a').find('h2').getText()#获取二级目录名称 
           subject2_dict={}
           
           for item in subject_wrapper.find('div',attrs={'class':'e-2880429693 list'}).find_all('a',attrs={'class':'e-2880429693 item separator'}):
                subject2_dict[item.getText()]= BASE_URL+item['href'] #获取二级目录名称，url
                
           subject_dict[c2] = subject2_dict
           
        category_hotword_plats[anchor] =  subject_dict 
          
    #print(category_hotword_plats)
    return category_hotword_dict,category_hotword_plats
            
# 解析热门分类内容 
"""
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
track_ids=[]
def get_vedio_url(title,albumId):
    url = 'http://www.ximalaya.com/revision/album'
    header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Cookie':'_xmLog=xm_1528372350671_ji4hfpanjstquv; trackType=web; x_xmly_traffic=utm_source%3A%26utm_medium%3A%26utm_campaign%3A%26utm_content%3A%26utm_term%3A%26utm_from%3A; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1528372334,1528372351; _ga=GA1.2.105022450.1528372351; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1528378517'
    }
    header['Referer']='http://www.ximalaya.com/'+title+'/'+albumId+'/'
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
            
    header['Referer']='http://www.ximalaya.com/'+title+'/'+albumId+'/'
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
            track_result[tarcks['trackName']]=tarcks['src']     
        except:
            continue
    return track_result
    


def main():
    data = get_vedio_url('youshengshu','2854032')
    print(data)
    print('总条数：%d' %len(data))

if __name__ == '__main__':
    main()
