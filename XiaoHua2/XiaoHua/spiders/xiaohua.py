# --coding:utf-8--
import scrapy
from XiaoHua.items import XiaohuaItem
from scrapy import Request
import re
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')



class Myspider(scrapy.Spider):
    name='XiaoHua'
    allowed_domains=['mmonly.cc']
    def start_requests(self):
        """
        重写 start_requests函数。
        用途：批量爬取多个标签页。
        """
        #一共有6页
        for i in range(1,67):
            url='http://www.mmonly.cc/mmtp/swmn/list_11_'+str(i)+'.html'
            yield Request(url,callback=self.parse_one)

    def parse_one(self,response):
        """
        输入：response
        输出：Request
        用途：提取页面上相册的标题和url，存放在item里。通过meta传给下一个处理函数
        """
        #创建一个大的list存储所有的item
        items=[]
        mylinks=response.css('div[class*=title]')
        for index,link  in enumerate(mylinks):
            item=XiaohuaItem()
            args=(index, link.css('div span a::attr(href)').extract(), link.css('div span a::text').extract())
            title=args[2]
            url=args[1]
            if(len(title)!=0):
                item['title']=title[0]
                item['siteURL']=url[0]
                items.append(item)
#        pattern=re.compile('<div class="title".*?<a.*?href="(.*?)">(.*?)</a></span></div>',re.S)
#        html=response.text
#        mains=re.findall(pattern,html)
#        for main in mains:
#            #创建实例,并转化为字典
#            item=XiaohuaItem()
#            item['siteURL']=main[0]
#            item['title']=main[1]
#            items.append(item)
            

        for item in items:
            #用meta传入下一层
            yield Request(url=item['siteURL'],meta={'item1':item},callback=self.parse_two)

    def parse_two(self,response):
        """
        输入：response
        输出：产生下一级爬虫。
        用途：提取页面上的页数。批量产生下一级爬虫。
        """
        #传入上面的item1
#        response.encoding=response.apparent_encoding
        item2=response.meta['item1']
#        source=requests.get(response.url)
#        html=source.text.decode().encode('utf-8')
        
        html=response.text
#        print(html)
        pattern=re.compile('共(.*?)页',re.S)
        Num=re.search(pattern,html).group(1)
        items=[]
        for i in range(1,int(Num)+1):
            item=XiaohuaItem()
            #构造每一个图片入口链接，以获取源码中的原图链接
            item['title']=item2['title']
            item['pageURL']=response.url[:-5]+'_'+str(i)+'.html'
            items.append(item)
        for item in items:
            yield Request(url=item['pageURL'],meta={'item2':item},callback=self.parse_three)

    def parse_three(self,response):
        """
        输入：response
        输出：item
        用途：
        获取页面上图片的具体网址，存放在item里。
        """
        item=XiaohuaItem()
        item3=response.meta['item2']
        #传入上面的item2
        pattern=re.compile('<li class="pic-down h-pic-down"><a target="_blank" class="down-btn" href=\'(.*?)\'>.*?</a>',re.S)
        URL=re.search(pattern,response.text).group(1)
        item['detailURL']=URL
        item['title']=item3['title']
        yield item