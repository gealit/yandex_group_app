# Generated by Django 4.1.2 on 2022-10-13 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_boardmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardmessage',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='boardmessage',
            name='image',
            field=models.ImageField(blank=True, upload_to='images', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='boardmessage',
            name='text',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]