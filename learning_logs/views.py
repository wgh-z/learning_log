"""定义url下数据的处理过程"""

from django.shortcuts import render


def index(request):
    """学习笔记的主页。"""
    return render(request, 'learning_logs/index.html')
