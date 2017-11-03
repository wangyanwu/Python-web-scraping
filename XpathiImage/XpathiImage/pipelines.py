# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import re 


class XpathiimagePipeline(object):
    def process_item(self, item, spider):
        return item
class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        """
        :param request: 每一个图片下载管道请求
        :param response:
        :param info:
        :param strip :清洗Windows系统的文件夹非法字符，避免无法创建目录
        :return: 每套图的分类目录
        """
        item = request.meta['item']
        folder = item['title']
        folder_strip = strip(folder)
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(folder_strip, image_guid)
        print(filename)
        return filename
    
    def get_media_requests(self, item,info):
        yield scrapy.Request(item['detailURL'],meta={'item': item})


    def item_completed(self,results,item,info):
        path=[x['path'] for ok,x in results if ok]
        if not path:
            raise DropItem('Item contains no images')
        print("function item_completed")
        print(u'正在保存图片：', item['detailURL'])
        print (u'主题', item['title'])
        yield item

        
def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path