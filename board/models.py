from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    foto = models.ImageField(upload_to='users_foto', blank=True, verbose_name='Фото')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class BoardMessage(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    text = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='images', blank=True, verbose_name='Картинка')
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CommentMessage(models.Model):
    board_message = models.ForeignKey(
        BoardMessage, on_delete=models.CASCADE, verbose_name='Пост', related_name='post_comments'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Ваш комментарий')
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.board_message} - {self.author} - {self.text[:10]}'
