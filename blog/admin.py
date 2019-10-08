from django.contrib import admin

from blog.models import Category, Post, Blogroll, Blogger


# 定制 Admin为 post显示详细信息
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Blogroll)
admin.site.register(Blogger)
