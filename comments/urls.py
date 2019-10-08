from django.conf.urls import url
from comments import views


urlpatterns = [
    url(r'^comment/post/(?P<post_pk>\d+)/$',views.post_comment,name='post_comment'),
]
