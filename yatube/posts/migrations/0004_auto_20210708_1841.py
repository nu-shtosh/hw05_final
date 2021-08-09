# Generated by Django 2.2.6 on 2021-07-08 15:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import posts.validators


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20210629_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='posts.Group'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(validators=[posts.validators.validate_not_empty], verbose_name='Text'),
        ),
    ]
