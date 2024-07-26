# django笔记

## 1. 创建项目

在当前目录创建名为ll_project的项目：

    django-admin startproject ll_project .

将生成manage.py文件和ll_project文件夹。

manage.py文件接受命令，用于管理项目。

ll_project文件夹用于存放项目文件。其中最重要的是 settings.py、urls.py 和 wsgi.py。
⽂件 settings.py 指定 Django 如何与系统交互以及如何管理项⽬。
在开发项⽬的过程中，我们将修改其中的⼀些设置，并添加⼀些设置。
⽂件 urls.py 告诉 Django，应创建哪些⽹⻚来响应浏览器请求。
⽂件wsgi.py 帮助 Django 提供它创建的⽂件，名称是 web server gateway interface
（Web 服务器⽹关接⼝）的⾸字⺟缩写。

### 1.1. 修改语言时区

在ll_project/settings.py文件中修改语言和时区：

    LANGUAGE_CODE = 'zh-hans'
    TIME_ZONE = 'Asia/Shanghai'

## 2. 运行项目

在当前文件夹下运行项目：

    python manage.py runserver

指定ip、端口

    python manage.py runserver 8001
    python manage.py runserver localhost:8001

## 3. 创建数据库

在当前文件夹下创建数据库：

    python manage.py migrate

将生成db.sqlite3文件。

## 4. 创建应用

在当前文件夹下创建名为learning_logs的应用：

    python manage.py startapp learning_logs

将生成learning_logs文件夹。其中最重要的⽂件是 models.py、admin.py 和 views.py。
我们将使⽤ models.py 来定义要在应⽤程序中管理的数据，稍后再介绍 admin.py 和 views.py。

### 4.1. 定义模型

在learning_logs/models.py文件中定义模型：

    from django.db import models

    class Topic(models.Model):
        """⽤户学习的主题"""
        text = models.CharField(max_length=200)
        date_added = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            """返回模型的字符串表示，即模型的名称。"""
            return self.text

### 4.2. 激活模型

在ll_project/settings.py文件中添加应用：

    INSTALLED_APPS = [
        'learning_logs',
    ]

### 4.3. 创建迁移

    python manage.py makemigrations learning_logs

### 4.4. 应用迁移（修改数据库）

    python manage.py migrate

每当需要修改“学习笔记”管理的数据时，都采取如下三个步骤：修改models.py，
对 learning_logs 调⽤ makemigrations，以及让 Django迁移项⽬。

## 5. 创建管理网站

### 5.1. 创建超级用户

在当前文件夹下创建超级用户：

    python manage.py createsuperuser

### 5.2. 管理网站注册模型

在learning_logs/admin.py文件中注册模型：

    from django.contrib import admin
    from .models import Topic

    admin.site.register(Topic)

现在可通过<http://localhost:8000/admin/>访问管理网站
