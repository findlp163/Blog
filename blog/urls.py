from django.conf.urls import url

from blog.views import IndexView, DetailPostView, CategoryView, ArchivesView, ArchivesPost, CategotysPostView
from blog.views import search

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),  # 主页
    url(r'^detail/(?P<pk>[0-9]+)/$',
        DetailPostView.as_view(), name='detail'),  # 详情页

    url(r'^category/(?P<pk>[0-9]+)/$',
        CategotysPostView.as_view(), name='category_post'),  # 主页-分类
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',
        ArchivesPost.as_view(), name='archives_post'),  # 主页-归档

    url(r'^category$', CategoryView.as_view(), name='category'),  # 分类
    url(r'^archives$', ArchivesView.as_view(), name='archives'),  # 归档

    url(r'^search/$', search, name='search'),  # 搜索

]
