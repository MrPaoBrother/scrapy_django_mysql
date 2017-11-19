#Headers 中间件

from douban.settings import UAPOOL #代理池

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random

class Uamid(UserAgentMiddleware):
    def __init__(self , user_agent=''):
        self.user_agent = user_agent
    def process_request(self, request, spider):
        thisua = random.choice(UAPOOL)
        print("当前使用的user-agent 是:" , thisua)
        request.headers.setdefault('User-Agent' , thisua)

