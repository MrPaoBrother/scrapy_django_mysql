# -*- coding: utf-8 -*-
import scrapy
from douban.items import DetailItem,CommentsItem
from movie.models import Detail,Comments
from scrapy.http import Request
import time
import re
import urllib.parse
class DbspdSpider(scrapy.Spider):
    name = 'dbspd'
    allowed_domains = ['douban.com']
    #start_urls = ['http://www.baidu.com/']

    page_start = 0
    page_limit = 50
    url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit='#%d&page_start=%d'

    def start_requests(self):
        print("Begin...")
        start_url = self.url + str(self.page_limit)+'&page_start='+str(self.page_start)
        yield Request(start_url,callback=self.parse)
    def parse(self, response):
         try:
             data = str(response.body.decode("utf8"))
             pat_name = '"title":"(.*?)"'
             pat_rate = '"rate":"(.*?)"'
             pat_url = '"url":"(.*?)"'
             names = re.compile(pat_name).findall(data)
             rates = re.compile(pat_rate).findall(data)
             urls = re.compile(pat_url).findall(data)
             item = DetailItem()
             item["mov_name"] = names
             item["mov_rate"] = rates
             item["mov_url"] = urls
             nums = len(item["mov_name"])
             if nums < 1:
                 print("=============================爬完了==================================")
                 return
                 exit(0)
             yield item
         except Exception as e:
             print("Error:",e)
             time.sleep(2) #缓两秒
         for i in range(2 , 250):
             next_start = (i-1)*self.page_limit
             next_limit = self.page_limit
             next_url = self.url + str(next_limit)+'&page_start='+str(next_start)
             next_url = urllib.parse.quote(next_url)
             next_url = urllib.parse.unquote(next_url)
             print("next_url:",next_url)
             print("================================正在爬取:%d页==============================="%i)
             yield Request(next_url, callback=self.parse ,
                           headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"})


