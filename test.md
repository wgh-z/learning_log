管理员账户：ll_admin
密码：123456

账户1：123
密码：test_123

### 9.3. 保护视图

在accounts/view.py文件中添加：

    from django.contrib.auth.mixins import LoginRequiredMixin

    class TopicListView(LoginRequiredMixin, ListView):
        model = Topic
        context_object_name = 'topics'

    class TopicDetailView(LoginRequiredMixin, DetailView):
        model = Topic
        context_object_name = 'topic'

    class EntryListView(LoginRequiredMixin, ListView):
        model = Entry
        context_object_name = 'entries'

    class EntryDetailView(LoginRequiredMixin, DetailView):
        model = Entry
        context_object_name = 'entry'

    class EntryCreateView(LoginRequiredMixin, CreateView):
        model = Entry
        fields = ['text']
        success_url = reverse_lazy('learning_logs:index')

        def form_valid(self, form):
            form.instance.topic = self.topic
            return super().form_valid(form)

    class EntryUpdateView(LoginRequiredMixin, UpdateView):
        model = Entry
        fields = ['text']
        success_url = reverse_lazy('learning_logs:index')

在accounts/admin.py文件中注册模型：

    from django.contrib import admin
from .models import User

admin.site.register(User)

在accounts/models.py文件中定义模型：

    from django.contrib.auth.models import AbstractUser

    class User(AbstractUser):
        pass

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
