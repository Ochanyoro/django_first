from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#カスタムユーザーモデルを使う
class CustomUser(AbstractUser):
    """ユーザー拡張モデル"""

    class Meta:
        verbose_name_plural = "CustomUser"
