from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    about = models.TextField(verbose_name='О себе', blank=True, null=True)

    def __str__(self):
        return self.username


class BoardMessage(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    text = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='images', blank=True, verbose_name='Картинка')
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
