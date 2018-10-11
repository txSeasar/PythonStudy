# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import os
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem

class ScrapefilePipeline(FilesPipeline):
    
    def get_media_requests(self, item,info):
        #for url in item["file_url"]:
            #yield scrapy.Request(url)
        print("xxxxcccxxxxxxxxxxxxxxxxxxx:"+item['downloadUrl'])
        yield scrapy.Request(item['downloadUrl'])
        
    def file_path(self, request, response=None, info=None):
        """
        重命名模块
        """
        path = request.url.split("/")
        fileName = os.path.join(path[len(path)-1])
        print("xxxxfilexxxxxxxxxxxxxxxxxxx:"+fileName)
        return fileName

    def item_completed(self, results, item, info):
        print('***      enter item           ****')
        print(item['downloadUrl']+'xxxxxx')
        for ok, x in results:
            print(ok)
            print(x)
            if not ok:
                raise DropItem("Item contains no files")
        return item
    
    