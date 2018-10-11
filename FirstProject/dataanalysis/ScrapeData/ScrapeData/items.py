# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapedataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    '''{"id":null,
        "secCode":"600231",
        "secName":"凌钢股份",
        "orgId":"gssh0600231",
        "announcementId":"1205488844",
        "announcementTitle":"2018年第三季度报告",
        "announcementTime":1539100800000,
        "adjunctUrl":"finalpage/2018-10-10/1205488844.PDF",
        "adjunctSize":849,
        "adjunctType":"PDF",
        "storageTime":null,
        "columnId":null,
        "pageColumn":null,
        "announcementType":null,
        "associateAnnouncement":"1205490224",
        "important":null,
        "batchNum":null,
        "announcementContent":null,
        "orgName":null,
        "announcementTypeName":null}'''
    
    secCode = scrapy.Field()
    secName = scrapy.Field()
    orgId = scrapy.Field()
    announcementId = scrapy.Field()
    announcementTitle = scrapy.Field()
    adjunctUrl = scrapy.Field()
    adjunctType = scrapy.Field()
    downloadUrl = scrapy.Field()
    
    #file_urls = scrapy.Field()

    
    