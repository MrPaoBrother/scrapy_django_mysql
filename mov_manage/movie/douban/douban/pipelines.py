# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from movie.models import Detail,Comments

class DoubanPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'dbspd':
            print("Saving...")
            nums = len(item["mov_name"])
            for i in range(nums):
                mov_name = item["mov_name"][i]
                mov_rate = item["mov_rate"][i]
                print("name:",item["mov_name"][i])
                print("mov_rate:", item["mov_rate"][i])
                item["mov_url"][i] = item["mov_url"][i].replace("\\" , "")
                print("mov_url:", item["mov_url"][i])
                mov_url = item["mov_url"][i]
                mov = Detail(
                    mov_name = mov_name,
                    mov_rate = mov_rate,
                    mov_url = mov_url
                )
                mov.save()
            print("Save Success!")
            return item
        elif spider.name is 'dbcommentspd':
            print("Saving...")
            try:
                nums = len(item["comment_user"])
                for i in range(nums):
                    mov_id = item["mov_id"]
                    comment_user = item["comment_user"][i]
                    comment_time = item["comment_time"][i]
                    comment_like = item["comment_like"][i]
                    comment_content = item["comment_content"][i]
                    print("content:" , comment_content)
                    comment = Comments(
                        mov_id = mov_id,
                        comment_user=comment_user,
                        comment_time = comment_time,
                        comment_like=comment_like,
                        comment_content=comment_content,
                    )
                    try:
                        comment.save()
                    except Exception as e:
                        print(e)
                        print("存储出错了...")
                print("Save Success!")
                return item
            except Exception as e:
                print(e)
            pass
        else:
            pass
