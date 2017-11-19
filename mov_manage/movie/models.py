from django.db import models

# Create your models here.

#电影详情
class Detail(models.Model):
    mov_name = models.CharField(max_length=50)
    mov_rate = models.CharField(max_length=10)
    mov_url = models.CharField(max_length=100)#链接url
    def __str__(self):
        return self.mov_name



#电影评论信息
class Comments(models.Model):
    mov_id = models.ForeignKey(Detail)#mov_id是对应每一部电影
    comment_user = models.CharField(max_length=50)
    comment_time = models.CharField(max_length=50)
    comment_like = models.CharField(max_length=10)#用户点赞
    comment_content = models.TextField(default="存在乱码") #用户评论内容

    def __str__(self):
        return self.comment_content