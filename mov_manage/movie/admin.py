from django.contrib import admin
from movie.models import Detail,Comments
# Register your models here.


class CommentsInline(admin.StackedInline):
    model = Comments
    extra = 2


class DetailAdmin(admin.ModelAdmin):
    #fields = ['mov_name' , 'mov_rate' , 'mov_url']
    fieldsets = [
        ("影片名字" , {'fields':['mov_name']}),
        ("评分" , {'fields':['mov_rate']}),
        ("链接" , {'fields':['mov_url']}),
    ]
    inlines = [CommentsInline]
    search_fields = ['mov_name']
    list_display = ['mov_name' , 'mov_rate' , 'mov_url']
admin.site.register(Detail , DetailAdmin)
admin.site.register(Comments)