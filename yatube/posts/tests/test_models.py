from django.test import TestCase
from posts.models import Group, Post, User


class PostModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Создаём тестовую запись в БД."""
        cls.user = User.objects.create_user('Геральт из Ривии')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user
        )

    def test_str(self):
        """Проверяем что у str правильный вывод."""
        post = str(PostModelTest.post)
        expected_value = 'Тестовый текст'
        self.assertEqual(
            post,
            expected_value,
            '__str__ работает неправильно.')


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Создаём тестовую запись в БД."""
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test_group',
            description='Тестовое описание текста'
        )

    def test_str(self):
        """Проверяем что у str правильный вывод."""
        group = str(GroupModelTest.group)
        expected_value = 'Тестовый заголовок'
        self.assertEqual(
            group,
            expected_value,
            '__str__ работает неправильно.')
