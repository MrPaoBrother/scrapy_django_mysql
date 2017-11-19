# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
import urllib.request as req
from douban.items import DetailItem,CommentsItem
from movie.models import Detail,Comments
import urllib.parse
import urllib.request as req
import re
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码
def getCommentNums(url):
    try:
        headers = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"
        request = req.Request(url)
        request.add_header("User-Agent",headers)
        with req.urlopen(request) as o:
            data = str(o.read().decode("utf8"))
            pat = '<a href=".*?">全部(.*?)条</a>'
            result = re.compile(pat, re.S).findall(data)[0]
            print("Result:",result)
            nums = int(result)
        return nums

    except Exception as e:
        print(e)
class DbcommentspdSpider(scrapy.Spider):
    name = 'dbcommentspd'
    allowed_domains = ['douban.com']
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
    start = 0
    limit = 20
    url_index = 0 #爬到了第几个电影的index
    pk =  Detail.objects.all()[url_index].id
    def start_requests(self):
        login_url = "https://accounts.douban.com/login"
        return [Request(login_url , callback=self.parse , meta={"cookiejar":1} , headers=self.header)]

    def parse(self, response):
        captcha = response.xpath("//img[@id='captcha_image']/@src").extract()
        url = Detail.objects.all()[self.url_index].mov_url + "comments?start=" + str(self.start) + "&limit=" + str(self.limit)
        if len(captcha) > 0:
            print("有验证码")
            loaclpath = "G:\MyPythonWork\mov_manage\movie\douban\douban\images\code.png"
            req.urlretrieve(captcha[0] , filename=loaclpath)
            value = input("输入验证码:")
            data = {
                "form_email":"18702604589",
                "form_password":"13672240290cccc",
                "captcha-solution":value,
                "redir": url
            }
            print("输入的验证码为:%s"%(value))
        else:
            print("没有验证码")
            data = {
                "form_email": "18702604589",
                "form_password": "13672240290cccc",
                "redir": url
            }
        print("登陆中...")
        print(url)
        return [FormRequest.from_response(
            response,
            meta = {"cookiejar":response.meta["cookiejar"]},
            headers = self.header,
            formdata=data,
            callback=self.next,
        )]
    def next(self , response):
        try:
            data = str(response.body.decode("utf8"))
            print("登陆成功...")
            users = response.xpath('//div[@class="comment"]//span[@class="comment-info"]/a/text()').extract()
            pat_times = '<span class="comment-time " title="(.*?)">'
            times = re.compile(pat_times , re.S).findall(data)
            pat_likes = '<span class="votes">(.*?)</span>'
            likes = re.compile(pat_likes , re.S).findall(data)

            #pat_contents = '<p class="">(.*?)</p>'
            #contents = re.compile(pat_contents  , re.S).findall(data)
            contents = response.xpath('//div[@class="comment"]//p[@class=""]/text()').extract()
            #print("Length:",len(contents))
            pk = Detail.objects.all()[self.url_index].id #每一部电影的id
            print("pk=",pk)
            item = CommentsItem()
            item["mov_id"] = Detail.objects.get(pk=pk)
            item["comment_user"] = users
            item["comment_time"] = times
            item["comment_like"] = likes
            item["comment_content"] = contents
            yield item
            while Detail.objects.get(pk = self.pk):
                print("正在爬取《",Detail.objects.get(pk = self.pk).mov_name,"》")
                for i in range(2,100):
                    self.start = (self.limit)*(i-1)
                    next_url = Detail.objects.all()[self.url_index].mov_url + "comments?start=" + str(self.start) + "&limit=" + str(self.limit)
                    print("next_url:",next_url)
                    yield Request(next_url , callback=self.next ,headers=self.header)
                self.url_index = self.url_index + 1
                self.pk = self.pk + 1
                self.start = 0
                print("===============到了下一部电影《",Detail.objects.get(pk = self.pk).mov_name,"》=========")
        except Exception as e:
            print(e)
