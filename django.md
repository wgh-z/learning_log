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

## 6. 创建网页

数据库专家专注于模型，程序员专注于视图代码，⽽前端专家专注于模板

view视图：flask route装饰的函数，定义数据处理的过程
url：定义url和视图的映射关系
templates模板：html，渲染网页，定义数据展示的过程
model模型：定义数据存储的过程

### 6.1. 定义URL

在learning_logs/urls.py文件中定义URL：

    """定义 learning_logs 的 URL 模式"""

    from django.urls import path
    from . import views


    # 将应用的url定义在应用内，而不是在项目的urls.py中，方便管理
    app_name = 'learning_logs'
    urlpatterns = [
        # 主⻚
        path('', views.index, name='index'),
    ]

### 6.2. 定义view视图

在learning_logs/views.py文件中定义视图：

    """定义url下数据的处理过程"""

    from django.shortcuts import render


    def index(request):
        """学习笔记的主页。"""
        return render(request, 'learning_logs/index.html')

### 6.3. 创建templates模板

在learning_logs/templates/learning_logs文件夹中创建index.html文件：

    <p>学习笔记</p>

### 6.4 映射url

在ll_project/urls.py文件中映射url：

    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('learning_logs.urls')),
    ]

## 7. 模板继承

父模板：定义网站的通用元素，如导航栏
子模板：继承父模板，定义网站的具体内容

模板继承可以使代码更简洁，更易维护。
html语言中由于标签较多，缩进层级较多，一般使用2个空格缩进

[django模板语言](https://docs.djangoproject.com/zh-hans/5.0/ref/templates/language/)

### 7.1. 定义父模板

在learning_logs/templates/learning_logs文件夹中创建base.html文件：

    <p>
      <a href="{% url 'learning_logs:index' %}">学习笔记</a>
    </p>
    {% block content %}{% endblock content %}

- **`<a> </a>`** 表示通过href指向的超链接跳转到别的位置，这个超链接是在当前url的基础上叠加的。
- **`{% %}`** 为Django模板语言，用于在html中插入数据。
- **`{% url 'learning_logs:index' %}`**
    表示该url为learning_logs中名为index的url,
    这里的learning_logs是一个命名空间，为learning_logs/urls.py文件的app_name属性，不需要与应用文件夹名相同。
    index为learning_logs/urls.py文件的urlpatterns的name属性。
- **`{% block content %} ... {% endblock content %}`**
    表示该块为子模板可替换的块，且该块的名称为content，但并不是每个块都需要替换。
    因此可以定义多个块来预留空间，子模板中根据需要替换。
    块中间也可以定义内容，这些内容在子模板中不会被替换，除非子模板中定义了同名的块。
    如需替换该块，子模板中需要使用相同的块名。

### 7.2. 继承父模板

在learning_logs/templates/learning_logs文件夹中重写index.html文件：

    {% extends 'learning_logs/base.html' %}

    {% block content %}
      <p>学习笔记为你感兴趣的任何话题保留学习记录</p>
    {% endblock content %}

- **`{% extends %}`** 表示继承的父模板名，能够导入父模板中的所有内容。
- **`{% block content %} ... {% endblock content %}`** 表示替换父模板中名为content的块。

### 7.3. 模板中访问数据

在learning_logs/views.py文件中修改视图：

    def index(request):
        """学习笔记的主页。"""
        topics = Topic.objects.order_by('date_added')
        context = {'topics': topics}
        return render(request, 'learning_logs/index.html', context)

- **`Topic.objects.order_by('date_added')`** 查询数据库，按date_added字段排序，返回Topic对象列表。
- **`context = {'topics': topics}`** 表示将topics对象列表赋值给context字典的topics键。
- **`return render(request, 'learning_logs/index.html', context)`** 表示将context字典传递给index.html模板。

在learning_logs/templates/learning_logs/topics.html文件中定义模板：

    {% extends 'learning_logs/base.html' %}

    {% block content %}
    <p>主题</p>
    <ul>
        {% for topic in topics %}
        <li>{{ topic.text }}</li>
        {% empty %}
        <li>尚未添加主题</li>
        {% endfor %}
    </ul>
    {% endblock content %}

这里使用

    {% for item in list %}
    do something with each item
    {% endfor %}

语法来遍历列表中的每个元素。

- **`{{ variable }}`**表示变量。
- **`{% for topic in topics %}`** 表示遍历context中的topics列表中的每个元素。
- **`{{ topic.text }}`** 表示输出topic对象的text属性。属性在models.py中的Topic类定义。
- **`{% empty %}`** 表示如果topics列表为空，则执行该块中的内容。
- **`{% endfor %}`** 表示结束for循环。

### 7.4. 向url传递数据

在learning_logs/urls.py文件中定义url：

    path('topics/<int:topic_id>/', views.topic, name='topic'),

- **`<int:topic_id>`** 表示该url匹配一个整数参数，并将该参数赋给topic_id，在视图函数中作为实参。
- **`path('topics/<int:topic_id>/', views.topic, name='topic')`** 表示该url调用的视图函数为topic，该url的名称为topic。

在learning_logs/views.py文件中定义视图：

    def topic(request, topic_id):
        """显示单个主题及其所有的条目。"""
        topic = Topic.objects.get(id=topic_id)
        ...

在learning_logs/templates/learning_logs/topic.html文件中定义模板：

    {% extends 'learning_logs/base.html' %}

    {% block content %}
    <p>主题: {{ topic.text }}</p>
    <p>条目:</p>
    <ul>
        {% for entry in entries %}
        <li>
            <p>{{ entry.date_added|date:'M d, Y H:i' }}</p>
            <p>{{ entry.text|linebreaks }}</p>
        </li>
        {% empty %}
        <li>该主题下没有任何条目</li>
        {% endfor %}
    </ul>
    {% endblock content %}

- **`|`** 表示过滤器，即一种处理函数，类似于视频图像处理中的掩膜。
- **`|date:'M d, Y H:i'`** 表示将date_added属性格式化为3字母月（中文下不同）、2位日、4位年、2位24小时、2位分。
- **`|linebreaks`** 表示将text属性中的换行符转换为html中的换行标签。

[django过滤器](https://docs.djangoproject.com/zh-hans/5.0/ref/templates/builtins/#ref-templates-builtins-filters)

修改learning_logs/templates/learning_logs/topics.html文件：

    <li>
        <a href="{% url 'learning_logs:topic' topic.id %}">
        {{ topic.text }}
        </a>
    </li>

- **`{% url 'learning_logs:topic' topic.id %}`** 表示使用learning_logs命名空间中名为topic的url模式，并将topic.id作为实参。这里既可以用位置参数，也可以使用关键字参数:
`{% url 'learning_logs:topic' topic_id=topic.id %}`

## 8. 静态文件

静态文件：css、js、图片等

### 8.1. 创建静态文件夹

在learning_logs/static/learning_logs文件夹中创建index.html文件：

    <p>学习笔记</p>

### 8.2. 映射静态文件

在ll_project/settings.py文件中映射静态文件：

    STATIC_URL = '/static/'

    # 添加静态文件夹
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]

### 8.3. 引用静态文件

在learning_logs/templates/learning_logs/index.html文件中引用静态文件：

    <link rel="stylesheet" href="{% static 'learning_logs/style.css' %}">

## 9. 创建其他网页

### 9.1. 定义URL

在learning_logs/urls.py文件中定义URL：

    """定义 learning_logs 的 URL 模式"""

    from django.urls import path
    from . import views


    # 将应用的url定义在应用内，而不是在项目的urls.py中，方便管理
    app_name = 'learning_logs'
    urlpatterns = [
        # 主⻚
        path('', views.index, name='index'),
        path('topics/', views.topics, name='topics'),
    ]

### 9.2. 定义view视图

在learning_logs/views.py文件中定义视图：

    """定义url下数据的处理过程"""

    from django.shortcuts import render


    def topics(request):
        """学习笔记的主页。"""
        return render(request, 'learning_logs/topics.html')
