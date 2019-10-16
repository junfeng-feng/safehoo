# encoding=utf-8
import re
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
import logging
import json
import copy
import time
import uuid
import sys

from dianping.items import DianpingItem

class SpiderTmallShop(Spider):
    name = 'dianping'
    allowed_domain = ['safehoo.com']
    start_urls = []
    #分页数据
    #for pageNo in range(1, 100):
    for pageNo in range(1, 2):
        #start_urls.append("http://www.safehoo.com/Case/Case/Collapse/List_%s.shtml" % (pageNo))
        #物理打击
        start_urls.append("http://www.safehoo.com/Case/Case/Hit/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Vehicle/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Machine/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Crane/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Blow/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Blaze/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Drop/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Collapse/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Boiler/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Container/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Mine/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Poison/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Drowned/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Air/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Electric/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Scorch/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Case/Other/List_%s.shtml" % (pageNo))
        start_urls.append("http://www.safehoo.com/Case/Stat/List_%s.shtml" % (pageNo))
        
    def __init__(self):
        self.hourRe = re.compile("([1-9]|[0-9]{1,2}) *(时|点)")
        self.numberRe = re.compile("[0-9]+")
        self.noonRe = re.compile("上午|下午|凌晨|早上|晚上|清早|傍晚|深夜|夜里|正午|黄昏")
        pass
    
    def parse(self, response):
        #copy.deepcopy(response)
        #select = response

        item = DianpingItem()
        item["accidentName"] = ""
        item["country"] = ""
        item["province"] = ""
        item["accidentClass"] = ""
        item["accidentType"] = ""
        item["accidentDate"] = ""
        item['accidentNoon']= ""
        item["accidentHour"] = ""
        item["accidentDescription"] = ""

        typeList = response.xpath("""//div[@class='l_dh']//a""")
        if len(typeList) > 0:
            item["accidentType"] = typeList[-1].xpath(".//text()").extract()[0]
        
        #找到事故列表
        trList = response.xpath(""".//div[@class='childclass_content']//li""") 
         
        for  tr in trList:  #[1:]跳过标题行
#             try:
#                 item["accidentName"] = tr.xpath(".//font/text()").extract()[0]
#             except Exception as e:
#                 print(e)
#             if len(item["accidentName"]) == 0:
#                 item["accidentName"] = tr.xpath(".//text()").extract()[0]
#             try:
#                 item["country"] = tr.xpath(".//td[2]/text()").extract()[0]
#             except Exception as e:
#                 print(e)
#             try:
#                 item["province"] = tr.xpath(".//td[3]/text()").extract()[0]
#             except Exception as e:
#                 print(e)
#             try:
#                 item["accidentClass"] = tr.xpath(".//td[4]/text()").extract()[0]
#             except Exception as e:
#                 print(e)
#             try:
#                 item["accidentType"] = tr.xpath(".//td[5]/text()").extract()[0]
#             except Exception as e:
#                 print(e)
#             try:
#                 item["accidentDate"] = tr.xpath(".//td[6]/text()").extract()[0]
#             except Exception as e:
#                 print(e)

            descUrl = """http://www.safehoo.com/""" + tr.xpath(".//a/@href").extract()[0]
            request = Request(descUrl, callback=self.parseDescription, priority=123)
            request.meta["accident"] = copy.deepcopy(item)
            #print(item)
            yield request
            
        pass
            
    #pasre content
    def parseDescription(self, response):
        #item['accidentDescription'] = select.xpaht("""//*[@id="wrapper"]/div[3]/div[1]/div[2]/div[3]/div/p[1]""").extract()
        #print("parseDescription----")
        item = response.meta['accident']
        
        try:
            item["accidentName"] = response.xpath(".//div[@class='c_title_text']/h1/span/text()").extract()[0]
        except Exception as e:
            print(e)
#         index = response.url.find("id=")
#         item['accidentId'] = response.url[index+3:]
        item['accidentId'] = "-".join(self.numberRe.findall(response.url))
        desc = ""
        try:
            desc = "".join(response.css(".c_content_text").xpath(".//text()").extract())
        except Exception as e:
            print(e)

        try:
            hour = self.hourRe.search(desc)
            if hour:
                item["accidentHour"] = hour.group()
        except Exception as e:
            print(e)
        try:
            noon = self.noonRe.search(desc)
            if noon:
                item["accidentNoon"] = noon.group()
        except Exception as e:
            print(e)

        item["accidentDescription"] = desc
        yield item
        pass


