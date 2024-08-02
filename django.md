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

### 6.1. 定义URL模式

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

## 8. 数据传递

### 8.1. 模板中访问数据

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

### 8.2. 向url传递数据

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

### 8.3. 使用表单

表单是HTML页面中的一种元素，用于向服务器提交数据。在Django中，可以使用表单类来创建表单，并使用模板来显示表单。

#### 8.3.1. 新主题页面

在learning_logs/forms.py文件中创建表单：

    from django import forms
    from .models import Topic, Entry

    class TopicForm(forms.ModelForm):
        class Meta:
            model = Topic
            fields = ['text']
            labels = {'text': ''}

- **`model = Topic`** 表示将使用Topic模型创建表单，表单将符合模型要求。
- **`fields = ['text']`** 表示该表单将包含text字段。
- **`labels = {'text': ''}`** 表示该表单将不显示text字段的标签。

在learning_logs/view.py文件中添加：

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

**GET请求**：从服务器读取数据
**POST请求**：向服务器提交数据
在⽤户初次请求该⽹⻚时，浏览器将发送 GET 请求，此时不使用数据创建表单，即空表单，供用户填写；
在⽤户填写并提交表单时，浏览器将发送 POST 请求，此时数据被赋给request.POST。

⽅法`is_valid()`核实⽤户填写了所有必不可少的字段（表单字段默认都是必不可少的），⽽且输⼊的数据与要求的字段类型⼀致（例如，字段`text`少于200个字符，这是在models.py中指定的）
当⽤户提交的表单数据⽆效时，将显⽰⼀些默认的错误消息

在learning_logs/templates/learning_logs/new_topic.html文件中显示表单：

    {% extends "learning_logs/base.html" %}

    {% block content %}
    <p>添加一个新主题:</p>
    <form action="{% url 'learning_logs:new_topic' %}" method='post'>
        {% csrf_token %}
        {{ form.as_div }}
        <button name="submit">添加主题</button>
    </form>
    {% endblock content %}

- **`<form></form>`** 定义一个html表单，action表示数据发送的目标url，这里将发送到视图new_topic，method表示数据发送的方式，这里使用POST。

- **`{% csrf_token %}`** 表示添加一个跨站请求伪造（Cross-Site Request Forgery，简称CSRF）令牌，以防止恶意用户提交表单。
- **`as_div`** 让 Django 将所有表单元素都渲染为 HTM`<div></div>` 元素，这是区块标签，是⼀种整洁地显⽰表单的简单⽅式。

在learning_logs/templates/learning_logs/topics.html文件中添加链接：

    --snip--
    <a href="{% url 'learning_logs:new_topic' %}">添加一个新主题</a>
    {% endblock content %}

#### 8.3.2. 新条目页面

在learning_logs/forms.py文件中创建表单：

    class EntryForm(forms.ModelForm):
        class Meta:
            model = Entry
            fields = ['text']
            labels = {'text': ''}
            widgets = {'text': forms.Textarea(attrs={'cols': 80})}

- **`widgets = {'text': forms.Textarea(attrs={'cols': 80})}`** 一种表单元素，表示将text字段渲染为文本域，并设置文本域的宽度为80个字符。

在learning_logs/urls.py文件中添加：

    # ⽤于添加新条⽬的⻚⾯
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),

在learning_logs/view.py文件中添加：

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

在learning_logs/templates/learning_logs/new_entry.html文件中显示表单：

    {% extends "learning_logs/base.html" %}

    {% block content %}
    <p>
        <a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a>
    </p>
    <p>添加一个新条目:</p>
        <form action="{% url 'learning_logs:new_entry' topic.id %}" method='post'>
        {% csrf_token %}
        {{ form.as_div }}
        <button name='submit'>添加条目</button>
    </form>
    {% endblock content %}

这里的`topic`是由view.py中的`context`字典传递过来
第一条指向topic的url用于返回topic页面

在learning_logs/templates/learning_logs/topic.html文件条目字段后添加链接：

    <p>
        <a href="{% url 'learning_logs:new_entry' topic.id %}">添加新条目</a>
    </p>





## 9. 用户账户和数据

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
`