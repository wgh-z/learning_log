"""定义 learning_logs 的 URL 模式"""

from django.urls import path
from . import views


# 将应用的url定义在应用内，而不是在项目的urls.py中，方便管理
app_name = 'learning_logs'
urlpatterns = [
    # 主⻚
    path('', views.index, name='index'),
]
