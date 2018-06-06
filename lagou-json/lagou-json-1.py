# encoding=utf-8
import requests
import codecs
import json
from bs4 import BeautifulSoup
#爬取拉钩网最新的30页数据
def get_data():
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Cookie':'WEBTJ-ID=20180606175235-163d4832a9f738-0012e4d7cdf564-737356c-1327104-163d4832aa0120; _ga=GA1.2.644601090.1528278756; _gid=GA1.2.1258057392.1528278756; user_trace_token=20180606175519-b890b383-696f-11e8-9379-5254005c3644; LGUID=20180606175519-b890b6c8-696f-11e8-9379-5254005c3644; JSESSIONID=ABAAABAABEEAAJAF0A6E4E448BC3B3F5322D410EE4F2FDD; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search; _gat=1; LGSID=20180606183708-904940bb-6975-11e8-9272-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DqsTn6tD-BxudBMBe9a3hQRHOu7R5auHtV0G7R0AxbKwCQTqeA6BQE4iN9j1uY-k0%26wd%3D%26eqid%3Da96c099c00022dff000000065b17b3b6; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F147.html; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528278791,1528279832,1528279837,1528281266; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528281275; LGRID=20180606183718-95dd100e-6975-11e8-9379-5254005c3644; SEARCH_ID=d89dfe80afe645c2b1c8feb45e0b84d3'
        ,'Referer':'https://www.lagou.com/jobs/list_?labelWords=&fromSearch=true&suginput='
    }
    url='https://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false'
    formData={'pn':'1','kd':'','first':'true'}
    i = 0
    while(True):
        data = requests.post(url, headers=headers,params=formData).json()['content']
        parse_json(data)
        i = i+1
        formData={'pn':i,'kd':'','first':'true'}
        if(i==30):
            break
       
       
    

def parse_json(data):
    dat = data['positionResult']
    result = dat['result']
    positionName=[]
    workYear = []
    education = []
    jobNature = []
    createTime = []
    city = []
    salary = []
    positionAdvantage = []
    financeStage = []
    firstType = []
    secondType = []
    for dic in result:
        positionName.append(dic['positionName'])
        workYear.append(dic['workYear'])
        education.append(dic['education'])  
        jobNature.append(dic['jobNature'])
        createTime.append(dic['createTime'])
        city.append(dic['city'])
        salary.append(dic['salary'])
        positionAdvantage.append(dic['positionAdvantage'])
        financeStage.append(dic['financeStage'])
        firstType.append(dic['firstType'])
        secondType.append(dic['secondType'])
    #这里可以自己想办法写入文件
    with open('c://Users/GuiRunning/Desktop/python-learn/lagou-json/lagou.txt', 'a') as fp:
        for i in range(len(positionName)):
            try:
                item = positionName[i]+'\t'+workYear[i]+'\t'+education[i]+'\t'+jobNature[i]+'\t'+createTime[i]+'\t'+city[i]+'\t'+salary[i]+'\t'+positionAdvantage[i]+'\t'+financeStage[i]+'\t'+firstType[i]+'\t'+secondType[i]
                fp.write(item+'\n')
                print(item)
            except:
                continue  
def main():
    get_data()
    
if __name__ == '__main__':
    main()




