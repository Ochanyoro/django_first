from django.contrib import admin
from .models import Diary
# Register your models here.

#日記テーブルを管理サイトで編集できるように
admin.site.register(Diary)
