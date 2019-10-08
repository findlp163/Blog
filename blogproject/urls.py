from django.conf import settings
from django.conf.urls import url, include, static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('blog.urls', namespace='blog')),  # blog路由
    url(r'', include('comments.urls', namespace='comments')),  # 评论路由
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),  # 富文本路由
    url(r'', include('users.urls', namespace='oauth')),  # 用户登录/授权路由
]

# 显示富文本上传图片
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
