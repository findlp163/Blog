from django.conf.urls import url
from users.views import qq_login, qq_check, is_login, logout

urlpatterns = [
    url(r'^oauth/qq/login/$', qq_login, name='qq_login'),
    url(r'^oauth/qq/check$', qq_check, name='qq_check'),
    url(r'^is_login/$', is_login, name='is_login'),
    url(r'^logout/$', logout, name='logout'),

    # url(r'^oauth/bind/account/$', qq_login, name='bind_account'),
]
