"""定义 learning_logs 的 URL 模式"""

from django.urls import path
from . import views


# 将应用的url定义在应用内，而不是在项目的urls.py中，方便管理
app_name = 'learning_logs'
urlpatterns = [
    # 主⻚
    path('', views.index, name='index'),

    # 显⽰所有主题的⻚⾯
    # 新url模式为topics/，匹配topics/和topics，但topic/后不能再接其他内容
    path('topics/', views.topics, name='topics'),

    # 特定主题的详细⻚⾯
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    # ⽤于添加新主题的⽹⻚
    path('new_topic/', views.new_topic, name='new_topic'),

    # ⽤于添加新条⽬的⻚⾯
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
]
