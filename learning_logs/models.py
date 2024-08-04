from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    """用户学习的主题"""

    # 使用charfield存储少量文本，数据库中预留200字符长度
    text = models.CharField(max_length=200)

    # 使用datetimefield记录日期和时间，
    # auto_now_add=True表示在对象创建时自动添加当前日期和时间
    date_added = models.DateTimeField(auto_now_add=True)
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # print实例时自动调用这个方法
    def __str__(self):
        """返回模型的字符串表示"""
        return self.text


class Entry(models.Model):
    """学到的有关某个主题的具体知识"""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回⼀个表⽰条⽬的简单字符串"""
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return self.text
