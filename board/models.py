from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model inherited from AbstractUser for the ability to extend model"""
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    foto = models.ImageField(upload_to='users_foto', blank=True, null=True, verbose_name='Фото')

    class Meta:
        ordering = ('-last_login',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class BoardMessage(models.Model):
    """This model for the posts on the board"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    text = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='images', blank=True, verbose_name='Картинка')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ('-date_updated',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title


class CommentMessage(models.Model):
    """Comments will be shown with a chosen post"""
    board_message = models.ForeignKey(
        BoardMessage, on_delete=models.CASCADE, verbose_name='Пост', related_name='post_comments'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Ваш комментарий')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено', blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено', blank=True, null=True)

    class Meta:
        ordering = ('date_added',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.board_message} - {self.text[:30]} . . .'
