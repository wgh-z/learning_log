"""定义url下数据的处理过程"""

from django.shortcuts import render, redirect
from .models import Topic
from .forms import TopicForm


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

def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 刚进入new_topic网页，未提交数据：创建⼀个空表单
        form = TopicForm()
    else:
        # POST 提交的数据：对数据进⾏处理
        form = TopicForm(data=request.POST)
        if form.is_valid():  # 数据检查，表单有效
            form.save()  # 写入数据库
            return redirect('learning_logs:topics')  # 保存好⽤户提交的数据后，重定向到⽹⻚topics

    # 显⽰空表单或指出表单数据⽆效
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)  # 进入new_topic网页
