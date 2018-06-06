# encoding=utf-8
import requests
import codecs
import json
from bs4 import BeautifulSoup

def get_data():
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Cookie':'WEBTJ-ID=20180606175235-163d4832a9f738-0012e4d7cdf564-737356c-1327104-163d4832aa0120; _ga=GA1.2.644601090.1528278756; _gid=GA1.2.1258057392.1528278756; user_trace_token=20180606175519-b890b383-696f-11e8-9379-5254005c3644; LGUID=20180606175519-b890b6c8-696f-11e8-9379-5254005c3644; JSESSIONID=ABAAABAABEEAAJAF0A6E4E448BC3B3F5322D410EE4F2FDD; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search; _gat=1; LGSID=20180606183708-904940bb-6975-11e8-9272-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DqsTn6tD-BxudBMBe9a3hQRHOu7R5auHtV0G7R0AxbKwCQTqeA6BQE4iN9j1uY-k0%26wd%3D%26eqid%3Da96c099c00022dff000000065b17b3b6; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F147.html; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528278791,1528279832,1528279837,1528281266; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528281275; LGRID=20180606183718-95dd100e-6975-11e8-9379-5254005c3644; SEARCH_ID=d89dfe80afe645c2b1c8feb45e0b84d3'
        ,'Referer':'https://www.lagou.com/jobs/list_?labelWords=&fromSearch=true&suginput='
    }
    url='https://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false'
    formData={'pn':'1','kd':'','first':'true'}
    data = requests.post(url, headers=headers,params=formData).json()['content']
    parse_json(data) 

def parse_json(data):
    dat = data['positionResult']
    print(dat['result'])
    #这里可以自己想办法写入文件
    
    
     
def main():
    get_data()
    
if __name__ == '__main__':
    main()




