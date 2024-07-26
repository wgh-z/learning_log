from django.contrib import admin

# 在admin.py 所在的⽬录中查找 models.py
from .models import Topic, Entry


admin.site.register(Topic)
admin.site.register(Entry)
