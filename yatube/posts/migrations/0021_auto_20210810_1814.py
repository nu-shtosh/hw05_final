# Generated by Django 2.2.6 on 2021-08-10 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0020_auto_20210810_1811'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created',), 'verbose_name': 'Комментарии', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name': 'Подписки', 'verbose_name_plural': 'Подписки'},
        ),
    ]
