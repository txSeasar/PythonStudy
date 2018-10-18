# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 14:50:43 2018

@author: gaoyf
"""

import scrapy
import json
from ScrapeData.items import ScrapedataItem
from scrapy.http import Request,FormRequest

class MySpider(scrapy.Spider):
    
    #用于区别Spider
    name = "MySpider"
    #允许访问的域
    allowed_domains = ['cninfo.com.cn']
    #爬取的地址
    #start_urls 爬取网址,只适于不需要登录的请求，因为没法设置cookie等信息
    #start_urls = ["http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice-sse#"]
    #用start_requests()方法,代替start_urls
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}  #设置浏览器用户代理
    def start_requests(self):
        """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
        #http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice-sse#
        #http://uc.cninfo.com.cn/remoteUserInfo?callback=jsonpcallback1539140693594&method=jsonpcallback1539140693594&_=1539140693057
        return [Request('http://uc.cninfo.com.cn/remoteUserInfo?callback=jsonpcallback1539140693594&method=jsonpcallback1539140693594&_=1539140693057',meta={'cookiejar':1},callback=self.parse)]
        
    #爬取方法
    def parse(self, response):
        # 响应Cookie
        #Cookie1 = response.headers.getlist('Set-Cookie')   #查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
        
        print('登录中............')
        '''
        http://www.cninfo.com.cn/new/hisAnnouncement/query
        
        requestCookies
        JSESSIONID=A921EEF6FFF94E5DD1FF96C391CA8DBD; 
        noticeTabClicks=%7B%22szse%22%3A1%2C%22sse%22%3A0%2C%22hot%22%3A0%2C%22myNotice%22%3A0%7D; 
        tradeTabClicks=%7B%22financing%20%22%3A0%2C%22restricted%20%22%3A0%2C%22blocktrade%22%3A0%2C%22myMarket%22%3A0%2C%22financing%22%3Anull%7D; 
        JSESSIONID=A921EEF6FFF94E5DD1FF96C391CA8DBD; 
        _sp_ses.2141=*; 
        _sp_id.2141=e64cc4cd-3219-4446-b9bd-09268001f9b8.1539077238.6.1539304574.1539158177.4658a655-0728-4e16-a4a4-4a0533a38915
        
        formData
        pageNum: 1
        pageSize: 30
        tabName: fulltext
        column: szse
        stock: 
        searchkey: 
        secid: 
        plate: sz
        category: category_ndbg_szsh;category_bndbg_szsh;category_yjdbg_szsh;category_sjdbg_szsh;
        trade: 
        seDate: 2000-01-01 ~ 2018-10-12
        '''
        #simple request
        #req = Request('http://www.cninfo.com.cn/new/disclosure?column=sse_latest&pageNum=1&pageSize=20', 
        #              self.next, 
        #              dont_filter=True)
        #req.meta['cookiejar'] = response.meta['cookiejar']
        #req.cookies['_sp_id.2141'] = 'e64cc4cd-3219-4446-b9bd-09268001f9b8.1539077238.3.1539140696.1539084236.79065683-01aa-471b-87f8-b6e44e816fa8'
        
        for column,plate in [('sse','sz'),('szse','shmb')]:
            for page in range(7):
                req = FormRequest('http://www.cninfo.com.cn/new/hisAnnouncement/query', 
                              formdata={'pageNum':"'"+str(page)+"'",
                                    'pageSize':'30',
                                    'tabName':'fulltext',
                                    'column':"'"+column+"'",
                                    #'stock':'',
                                    'stock':'000725,gssz0000725;',
                                    'searchkey':'',
                                    'secid':'',
                                    'plate':"'"+plate+"'",
                                    'category':'category_ndbg_szsh;category_bndbg_szsh;category_yjdbg_szsh;category_sjdbg_szsh;',
                                    'trade':'',
                                    'seDate':'2000-01-01 ~ 2018-10-12'},
                              callback=self.next, 
                              dont_filter=True)
                req.meta['cookiejar'] = response.meta['cookiejar']
                req.cookies.update({'noticeTabClicks':'=%7B%22szse%22%3A1%2C%22sse%22%3A0%2C%22hot%22%3A0%2C%22myNotice%22%3A0%7D'})
                req.cookies.update({'tradeTabClicks':'%7B%22financing%20%22%3A0%2C%22restricted%20%22%3A0%2C%22blocktrade%22%3A0%2C%22myMarket%22%3A0%2C%22financing%22%3Anull%7D'})
                req.cookies.update({'_sp_ses.2141':'*'})
                req.cookies.update({'_sp_id.2141':'e64cc4cd-3219-4446-b9bd-09268001f9b8.1539077238.6.1539304574.1539158177.4658a655-0728-4e16-a4a4-4a0533a38915'})
                
                req.method = 'POST'
                #req.headers = self.header
                
                """第二次用表单post请求，携带Cookie、浏览器代理、用户登录信息，进行登录给Cookie授权"""
                """return [FormRequest.from_response(response,
                                                  url='http://www.cninfo.com.cn/new/disclosure?column=sse_latest&pageNum=1&pageSize=20',   #真实post地址
                                                  meta={'cookiejar':response.meta['cookiejar']},
                                                  headers=self.header,
                                                  formdata={'user':'','password':''},
                                                  callback=self.next,
                                                  )]"""
                #return [Request('http://www.cninfo.com.cn/new/disclosure?column=sse_latest&pageNum=1&pageSize=20',cookies=Cookie1,headers=self.header,callback=self.parse)]
                yield req
    
    def next(self,response):
        
        dataRet = json.loads(response.body.decode("utf-8"))
        print('#######################')
         #实例一个容器保存爬取的信息
        item = ScrapedataItem()  
        #for data in dataRet['classifiedAnnouncements']:
        for data in dataRet['announcements']:
            #获取每个div中的课程路径    
            #data = data[0]
            print("++++++++++"+data['secName'])
            #Get Normal report
            if '摘要' in data['announcementTitle'] or '正文' in data['announcementTitle']:
                continue
            
            #item['code'] = 'http://www.imooc.com' + box.xpath('.//@href').extract()[0]
            item['secCode'] = data['secCode']
            item['secName'] = data['secName']
            item['orgId'] = data['orgId']
            item['announcementId'] = data['announcementId']
            item['announcementTitle'] = data['announcementTitle']
            item['adjunctUrl'] = data['adjunctUrl']
            item['adjunctType'] = data['adjunctType']
            #http://www.cninfo.com.cn/finalpage/2018-09-26/1205465475.PDF
            item['downloadUrl'] = 'http://www.cninfo.com.cn/' +  data['adjunctUrl']
            #item['file_urls'] = 'http://www.cninfo.com.cn/' +  data['adjunctUrl']
            #返回信息
            yield item
            
    def next_bak(self,response):
        jieg = response.body.decode("utf-8") 
        print('登录响应结果：',jieg)
         #实例一个容器保存爬取的信息
        item = ScrapedataItem()  
        #这部分是爬取部分，使用xpath的方式选择信息，具体方法根据网页结构而定
        searchRetDiv = response.xpath('//div[@id="page-list-search"]')[0]
        #先获取每个结果的tr
        for box in searchRetDiv.xpath('//tr[@class="touch"]'):
            #获取每个div中的课程路径    
            #item['code'] = 'http://www.imooc.com' + box.xpath('.//@href').extract()[0]
            item['code'] = box.xpath('.//td[@class="sub-code"]/a/text()').extract()[0].strip()
            #获取div中的课程标题
            item['name'] = box.xpath('.//td[@class="sub-name"]/a/text()').extract()[0].strip()
           #获取div中的学生人数
            item['fileTitle'] = box.xpath('.//td[@class="sub-title"]/a/text()').extract()[0].strip()
             #获取div中的标题图片地址
            #item['fileUrl'] = 'http://www.cninfo.com.cn' + box.xpath('.//td[@class="sub-title"]/a/@href').extract()
            #返回信息
            yield item
        