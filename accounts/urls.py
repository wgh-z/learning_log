"""为应用程序 accounts 定义 URL 模式"""

from django.urls import path, include
from . import views


app_name = 'accounts'
urlpatterns = [
    # 使用 Django 内置的登录视图
    path('', include('django.contrib.auth.urls')),
    # 注册⻚⾯
    path('register/', views.register, name='register'),
]
