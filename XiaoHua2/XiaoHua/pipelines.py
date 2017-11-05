# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from XiaoHua import settings
import re



class XiaohuaPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        """
        :param request: 每一个图片下载管道请求
        :param response:
        :param info:
        :param strip :清洗Windows系统的文件夹非法字符，避免无法创建目录
        :return: 每套图的分类目录
        用途：重写file_path函数。用标题当目录，生成图片的存放路径。
        """
        item = request.meta['item']
        folder = item['title']
        folder_strip = strip(folder)
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(folder_strip, image_guid)
        print(filename)
        return filename
    
    def get_media_requests(self, item,info):
        #一定要把meta 传递下去。
        yield scrapy.Request(item['detailURL'],meta={'item':item})
        

    def item_completed(self,results,item,info):
        path=[x['path'] for ok,x in results if ok]
        if not path:
            raise DropItem('Item contains no images')
        print(u'正在保存图片：', item['detailURL'])
        print (u'主题', item['title'])
        return item
    
def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path
