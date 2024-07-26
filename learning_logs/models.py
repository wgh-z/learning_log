from django.db import models


class Topic(models.Model):
    """用户学习的主题"""

    # 使用charfield存储少量文本，数据库中预留200字符长度
    text = models.CharField(max_length=200)

    # 使用datetimefield记录日期和时间，
    # auto_now_add=True表示在对象创建时自动添加当前日期和时间
    date_added = models.DateTimeField(auto_now_add=True)

    # print实例时自动调用这个方法
    def __str__(self):
        """返回模型的字符串表示"""
        return self.text
