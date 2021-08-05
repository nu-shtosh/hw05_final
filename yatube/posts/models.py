from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_not_empty

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Текст', max_length=200)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        'Текст',
        help_text='Текст сюда!',
        validators=[validate_not_empty])
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='author_posts')
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='group_posts',
        help_text='Выбери группу из существующих!',
        verbose_name='Группа',
        blank=True,
        null=True)
    image = models.ImageField(
        upload_to='posts/',
        help_text='Давай картинку!',
        verbose_name='Изображение',
        blank=True,
        null=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_comment')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_comment')
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Оставьте свой комментарий!')
    created = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.text[:15]
