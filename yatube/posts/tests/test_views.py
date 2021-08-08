import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User


class PostsViewsTest(TestCase):
    """URL в рамках теста."""
    HOMEPAGE_URL = reverse('index')
    GROUP_URL = reverse('group_posts', kwargs={'slug': 'tslug'})
    GROUP_2_URL = reverse('group_posts', kwargs={'slug': 'tslug2'})
    PROFILE_URL = reverse('profile', kwargs={'username': 'tusername'})
    NEWPOST_URL = reverse('new_post')
    POSTEDIT_URL = reverse('post_edit', kwargs={
                           'username': 'tusername',
                           'post_id': '1'})
    POST_URL = reverse('post', kwargs={
                       'username': 'tusername',
                       'post_id': '1'})

    @classmethod
    def setUpClass(cls):
        """Создаем записи в БД."""
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.user = User.objects.create(
            first_name='tname',
            last_name='tlname',
            username='tusername',
            email='temail@yandex.ru'
        )
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=PostsViewsTest.small_gif,
            content_type='image/gif'
        )
        cls.group = Group.objects.create(
            title='ttitle',
            slug='tslug',
            description='tdescription'
        )
        cls.group_g = Group.objects.create(
            title='ttitle2',
            slug='tslug2',
            description='tdescription2'
        )
        cls.post = Post.objects.create(
            text='ttext',
            author=PostsViewsTest.user,
            group=PostsViewsTest.group,
            image=PostsViewsTest.uploaded
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        """Создаем клиентов."""
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.__class__.user)

    def test_pages_use_correct_template(self):
        """Проверяем URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            self.HOMEPAGE_URL: 'posts/index.html',
            self.PROFILE_URL: 'posts/profile.html',
            self.POST_URL: 'posts/post.html',
            self.POSTEDIT_URL: 'posts/new.html',
            self.NEWPOST_URL: 'posts/new.html',
            self.GROUP_URL: 'posts/group.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_new_context(self):
        """У new правильный context."""
        response = self.authorized_client.get(self.NEWPOST_URL)
        form_fields = {
            'group': forms.models.ModelChoiceField,
            'text': forms.CharField,
            'image': forms.ImageField,
        }
        for value in form_fields.items():
            with self.subTest(value=value):
                self.assertIn('form', response.context)

    def test_index_context(self):
        """У index правильный context."""
        response = self.guest_client.get(self.HOMEPAGE_URL)
        object = response.context['page'][0]
        expected_text = object.text
        expected_group = object.group

        self.assertEqual(expected_text, PostsViewsTest.post.text)
        self.assertEqual(expected_group.title, PostsViewsTest.group.title)

    def test_group_context_(self):
        """У group правильный context."""
        response = self.guest_client.get(self.GROUP_URL)
        object = response.context['group']
        expected_title = object.title
        expected_slug = object.slug
        expected_descrip = object.description

        self.assertEqual(expected_title, PostsViewsTest.group.title)
        self.assertEqual(expected_slug, PostsViewsTest.group.slug)
        self.assertEqual(expected_descrip, PostsViewsTest.group.description)

    def test_profile_context(self):
        """У profile правильный context."""
        response = self.guest_client.get(self.PROFILE_URL)
        object = response.context['author']
        expected_first_name = object.first_name
        expected_last_name = object.last_name
        expected_email = object.email

        self.assertEqual(expected_first_name, PostsViewsTest.user.first_name)
        self.assertEqual(expected_last_name, PostsViewsTest.user.last_name)
        self.assertEqual(expected_email, PostsViewsTest.user.email)

    def test_post_context(self):
        """У post правильный context."""
        response = self.guest_client.get(self.POST_URL)
        object = response.context['post']
        expected_author = object.author
        expected_text = object.text

        self.assertEqual(expected_author, PostsViewsTest.post.author)
        self.assertEqual(expected_text, PostsViewsTest.post.text)

    def test_post_edit_context(self):
        """У post_edit правильный context."""
        response = self.authorized_client.get(self.POSTEDIT_URL)
        form_fields = {
            'text': forms.CharField,
            'group': forms.models.ModelChoiceField,
            'image': forms.ImageField
        }
        for value in form_fields.items():
            with self.subTest(value=value):
                self.assertIn('form', response.context)

    def test_post_in_group(self):
        """Проверяем что пост в группе."""
        response = self.authorized_client.get(self.GROUP_URL)
        object = response.context['page'][0]
        expected_text = object.text
        expected_group = object.group
        expected_image = object.image

        self.assertEqual(expected_text, PostsViewsTest.post.text)
        self.assertEqual(expected_group.title, PostsViewsTest.group.title)
        self.assertEqual(expected_image, PostsViewsTest.post.image)

    def test_post_in_index(self):
        """Проверяем что пост на главной."""
        response = self.authorized_client.get(self.HOMEPAGE_URL)
        object = response.context['page'][0]
        expected_text = object.text
        expected_image = object.image

        self.assertEqual(expected_text, PostsViewsTest.post.text)
        self.assertEqual(expected_image, PostsViewsTest.post.image)

    def test_post_in_profile(self):
        """Проверяем что пост на странице профиля."""
        response = self.authorized_client.get(self.PROFILE_URL)
        object = response.context['page'][0]
        expected_text = object.text
        expected_image = object.image

        self.assertEqual(expected_text, PostsViewsTest.post.text)
        self.assertEqual(expected_image, PostsViewsTest.post.image)

    def test_post_in_profile_post(self):
        """Проверяем что пост на странице поста профиля."""
        response = self.authorized_client.get(self.POST_URL)
        object = response.context['post']
        expected_text = object.text
        expected_image = object.image

        self.assertEqual(expected_text, PostsViewsTest.post.text)
        self.assertEqual(expected_image, PostsViewsTest.post.image)

    def test_post_not_in_group(self):
        """Проверяем что пост не в другой группе."""
        response = self.authorized_client.get(self.GROUP_2_URL)
        assert not response.context['page'].has_next()

    def test_index_cache(self):

        texttext = 'new-post-with-cache'

        self.post = Post.objects.create(
            text=texttext,
            author=PostsViewsTest.user,
            group=PostsViewsTest.group,
        )

        response = self.authorized_client.get(self.HOMEPAGE_URL)
        page = response.content.decode()
        self.assertNotIn(self.post.text, page)
        cache.clear()

        response = self.authorized_client.get(self.HOMEPAGE_URL)
        page = response.content.decode()
        self.assertIn(self.post.text, page)


class PaginatorViewsTest(TestCase):
    """URL в рамках теста."""
    PROFILE_URL = reverse('profile', kwargs={'username': 'testusername'})
    GROUP_URL = reverse('group_posts', kwargs={'slug': 'testgroup'})
    HOMEPAGE_URL = reverse('index')

    @classmethod
    def setUpClass(cls):
        """Создаем записи в БД."""
        super().setUpClass()
        cls.user = User.objects.create_user(username='testusername')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='testgroup',
            description='Тестовое описание текста'
        )
        Post.objects.bulk_create((Post(
            text='testtext',
            author=cls.user,
            group=cls.group)) for _ in range(13))

    def test_contains_x_records(self):
        """Проверяем что пажинатор правильно считает записи"""
        response = self.client.get(self.HOMEPAGE_URL)
        self.PAGE_HOME = len(response.context['page'])
        self.assertEqual(self.PAGE_HOME, 10)

        response = self.client.get(self.HOMEPAGE_URL + '?page=2')
        self.PAGE_HOME_2 = len(response.context['page'])
        self.assertEqual(self.PAGE_HOME_2, 3)

        response = self.client.get(self.GROUP_URL)
        self.PAGE_GROUP = len(response.context['page'])
        self.assertEqual(self.PAGE_GROUP, 10)

        response = self.client.get(self.PROFILE_URL)
        self.PAGE_PROFILE = len(response.context['page'])
        self.assertEqual(self.PAGE_PROFILE, 10)

