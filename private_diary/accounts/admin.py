from django.contrib import admin
from .models import CustomUser
# Register your models here.

#管理サイトで編集できるようにする
admin.site.register(CustomUser)
