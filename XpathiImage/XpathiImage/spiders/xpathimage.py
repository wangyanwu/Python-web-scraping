# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy

#import sys
from XpathiImage.items import XpathiimageItem
from scrapy.http import Request
import re
from scrapy import Selector

#sys.setdefaultencoding('utf-8')

class MyImageSpider(scrapy.Spider):
    name = "xpathimage"
    allowed_domains = ["www.javbu.cc"]
    
    
    def start_requests(self):
        '''
        输入：
        输出：启动爬虫
        用途：用于多页爬取。
        '''
        start_urls = ['https://www.javbus.cc/label/7l']
#        print(start_urls)
        for url in start_urls:
            
            yield Request(url,callback=self.parseOne)
#        start_urls = ['http://www.moko.cc/channels/post/23/1.html']
#        print(start_urls)
#        Request(start_urls,callback=self.parseOne)
    
    def parseOne(self, response):
        """
        输入：response
        输出:启动下一级爬虫。
        用途：将目录页的相册标题和src+url放到一个大的list里，启动下一级爬虫。
        """
#        src='http://www.moko.cc'
        items=[]
        
#        pattern=re.compile('<div class="cover" cover-text="(.*?)">.*?href="(.*?)".*?</div>',re.S)
##text='<div class="cover" cover-text="来一波小清新"><a href="/post/1270140.html" hidefocus="true" target="_blank"><img src2="http://img.mb.moko.cc/2017-10-20/cbf84483-0eb6-45e0-b1c1-80f18a210e5a.jpg" alt="迷醉儿作品《来一波小清新》"/></a></div>'
#        mains=re.findall(pattern,response.text)
#        for main in mains:
#            item={}
#            print(main)
#            item['title']=main[0]
#            item['siteURL']=src+main[1]
#            items.append(item)
#        mylinks=response.xpath('//div[contains(@class,"cover")]')
        mylinks=response.xpath('//a[contains(@class,"movie-box")]')
        
        for index,link  in enumerate(mylinks):
#item 必须在for循环中创建，由于字典不允许key重复。否则会items只会把最后一个写入字典中。
            item=XpathiimageItem()
#            args=(index, link.xpath('@cover-text').extract(), link.xpath('a/@href').extract())
            args=(index, link.xpath('@href').extract(), link.xpath('div/img/@title').extract())
            title=args[2]
#            print(type(title))
            url=args[1]
            if len(title)!=0:
                item['title']=url[0].split('/')[-1]+title[0]
                item['siteURL']=url[0]
#                print(item['title'],item['siteURL'])
                items.append(item)
#        print(items)
        for item in items:
            #用meta传入下一层
            print("wangyanwu",item['title'],item['siteURL'])
            yield Request(url=item['siteURL'],meta={'item1':item},callback=self.parseTwo)        
#        items['image_urls']=response.xpath('//div[@class="swipeboxEx"]/div[@class="list"]/a/img/@data-original').extract()
    
    def parseTwo(self,response):
        print("intoparseTwo")
#        divs = response.xpath('//p[contains(@class,"picBox")]')
        item=XpathiimageItem()
        item2=response.meta['item1']
#        picpattern=re.compile('<p class="picBox"><img src2="(http.*?)".*?</p>')
#        URLs=re.findall(picpattern,response.text)
#        for URL in URLs:
#            item['detailURL']=URL
#            item['title']=item2['title']
#            yield item
        coverurl=response.xpath('//a[contains(@class,"bigImage")]/@href').extract()
        URLs=response.xpath('//a[contains(@class,"sample-box")]/@href').extract()
        URLs.append(coverurl[0])
        for URL in URLs:
           item['detailURL']=URL
           item['title']=item2['title']
           yield item