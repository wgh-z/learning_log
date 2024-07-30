"""定义url下数据的处理过程"""

from django.shortcuts import render
from .models import Topic


def index(request):
    """学习笔记的主页。"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """显示所有的主题。"""
    topics = Topic.objects.order_by('date_added')  # 数据库查询，可先在django shell中测试
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """显示单个主题及其所有的条目。"""
    topic = Topic.objects.get(id=topic_id)  # 数据库查询
    entries = topic.entry_set.order_by('-date_added')  # 数据库查询，-表示降序
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
