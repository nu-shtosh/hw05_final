# Generated by Django 2.2.6 on 2021-08-02 16:05

import django.db.models.deletion
from django.db import migrations, models

import posts.validators


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_auto_20210802_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, help_text='Выбери группу из существующих!', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_posts', to='posts.Group'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, help_text='Давай картинку!', null=True, upload_to='posts/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(help_text='Текст сюда!', validators=[posts.validators.validate_not_empty], verbose_name='Текст'),
        ),
    ]
