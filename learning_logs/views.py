"""定义url下数据的处理过程"""

from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


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

def new_entry(request, topic_id): # 添加新条目
    """在特定主题中添加新条⽬"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 刚进入new_entry网页，未提交数据：创建⼀个空表单
        form = EntryForm()
    else:
        # POST 提交的数据：对数据进⾏处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # 创建⼀个新的条⽬对象，并将其赋给 new_entry，但不保存到数据库中
            new_entry = form.save(commit=False)  # commit=False表示暂时不写入数据库
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
        """编辑既有条⽬"""
        entry = Entry.objects.get(id=entry_id)
        topic = entry.topic

        if request.method != 'POST':
            # 初始请求：创建一个表单，使⽤当前条⽬填充，用户将看到既有的数据，并且能够进行编辑
            form = EntryForm(instance=entry)
        else:
            # POST 提交的数据：根据 request.POST 中的相关数据对其进行修改
            form = EntryForm(instance=entry, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('learning_logs:topic', topic_id=topic.id)

        context = {'entry': entry, 'topic': topic, 'form': form}
        return render(request, 'learning_logs/edit_entry.html', context)
