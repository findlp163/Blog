import time

from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from users import models
from users.models import Users, OAuthQQUser
from users.oauth_client import OAuthQQ


def qq_login(request):
    oauth_qq = OAuthQQ(settings.QQ_APP_ID, settings.QQ_APP_KEY, settings.QQ_RECALL_URL)
    # 获取 得到Authorization Code的地址
    url = oauth_qq.get_auth_url()

    # 重定向到授权页面
    return HttpResponseRedirect(url)


def qq_check(request):
    """登录之后，会跳转到这里。需要判断code和state"""
    request_code = request.GET.get('code')
    oauth_qq = OAuthQQ(settings.QQ_APP_ID, settings.QQ_APP_KEY, settings.QQ_RECALL_URL)

    # 获取access_token
    access_token = oauth_qq.get_access_token(request_code)
    time.sleep(0.05)  # 稍微休息一下，避免发送urlopen的10060错误
    open_id = oauth_qq.get_open_id()

    # 检查open_id是否存在
    qq_open_id = models.OAuthQQUser.objects.filter(openid=open_id)
    print(qq_open_id)

    if qq_open_id:
        # 存在则获取对应的用户，并登录
        user = qq_open_id[0].user
        request.session['user_id'] = user.id
        request.session['nickname'] = user.nickname
        return HttpResponseRedirect('/')
    else:
        # 不存在，则创建用户并绑定授权 直接跳转到主页
        infos = oauth_qq.get_qq_info()  # 获取用户信息
        user = Users()
        username = 'lp' + open_id  # 生成用户名
        nickname = infos['nickname']  # 获取用户昵称
        user.username = username
        user.nickname = nickname
        user.save()
        oauthqq = OAuthQQUser()
        user = Users.objects.get(username=username)
        oauthqq.user_id = user.id
        oauthqq.openid = open_id
        oauthqq.save()
        request.session['user_id'] = user.id
        request.session['nickname'] = user.nickname
        return HttpResponseRedirect('/')


# 验证登录
def is_login(requset):
    user_id = requset.session.get('user_id')
    users = Users.objects.filter(pk=user_id)
    data = {}
    if users.exists():
        data['is_login'] = True
        data['nickname'] = users[0].nickname
    else:
        data['is_login'] = False
    return JsonResponse(data)


# 退出登录
def logout(request):
    request.session.flush()
    return redirect(reverse('blog:index'))
