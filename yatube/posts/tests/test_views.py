import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Follow, Group, Post, User


class PostsViewsTest(TestCase):
    """URL/Записи в рамках теста."""
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
    TEST_USER = 'tusername'
    TEST_TITLE = 'ttitle'
    TEST_SLUG = 'tslug'
    TEST_DESCRIPTION = 'tdescription'
    TEST_TEXT = 'ttext'
    TEST_TITLE_2 = 'ttitle2'
    TEST_SLUG_2 = 'tslug2'
    TEST_DESCRIPTION_2 = 'tdescription2'

    @classmethod
    def setUpClass(cls):
        """Создаем записи в БД."""
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.user = User.objects.create(
            username=PostsViewsTest.TEST_USER
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
            title=PostsViewsTest.TEST_TITLE,
            slug=PostsViewsTest.TEST_SLUG,
            description=PostsViewsTest.TEST_DESCRIPTION
        )
        cls.group_g = Group.objects.create(
            title=PostsViewsTest.TEST_TITLE_2,
            slug=PostsViewsTest.TEST_SLUG_2,
            description=PostsViewsTest.TEST_DESCRIPTION_2
        )
        cls.post = Post.objects.create(
            text=PostsViewsTest.TEST_TEXT,
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

    def test_add_comment(self):
        """У comment правильный context."""
        response = self.authorized_client.get(self.POST_URL)
        form_fields = {
            'text': forms.CharField,
        }
        for value in form_fields.items():
            with self.subTest(value=value):
                self.assertIn('form', response.context)

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
        """Проверяем кэш index."""
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
    """URL/Записи в рамках теста."""
    PROFILE_URL = reverse('profile', kwargs={'username': 'testusername'})
    GROUP_URL = reverse('group_posts', kwargs={'slug': 'testgroup'})
    HOMEPAGE_URL = reverse('index')
    TEST_TITLE = 'testtitle'
    TEST_SLUG = 'testgroup'
    TEST_TEXT = 'testtext'

    @classmethod
    def setUpClass(cls):
        """Создаем записи в БД."""
        super().setUpClass()
        cls.user = User.objects.create_user(username='testusername')
        cls.group = Group.objects.create(
            title=PaginatorViewsTest.TEST_TITLE,
            slug=PaginatorViewsTest.TEST_SLUG
        )
        Post.objects.bulk_create((Post(
            text=PaginatorViewsTest.TEST_TEXT,
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


class TestFollow(TestCase):
    """URL/Записи в рамках теста."""
    FOLLOW_URL = reverse('follow_index')
    PROFILE_FOLLOW_URL = reverse(
        'profile_follow',
        kwargs={'username': 'author'})
    PROFILE_UNFOLLOW_URL = reverse(
        'profile_unfollow',
        kwargs={'username': 'author'})
    TEST_USER_1 = 'author'
    TEST_USER_2 = 'follower'
    TEST_USER_3 = 'unfollower'
    TEST_TEXT = 'ttext'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.create_user(TestFollow.TEST_USER_1)
        cls.user_2 = User.objects.create_user(TestFollow.TEST_USER_2)
        cls.user_3 = User.objects.create_user(TestFollow.TEST_USER_3)

        cls.guest_client = Client()
        cls.authorized_author = Client()
        cls.authorized_author.force_login(cls.user_1)
        cls.authorized_follower = Client()
        cls.authorized_follower.force_login(cls.user_2)
        cls.authorized_unfollower = Client()
        cls.authorized_unfollower.force_login(cls.user_2)

        cls.post = Post.objects.create(
            text=TestFollow.TEST_TEXT,
            author=cls.user_1)

    def test_follow(self):
        """Проверяем что подписка работает."""
        self.authorized_follower.get(self.PROFILE_FOLLOW_URL)

        following_count = Follow.objects.filter(user=self.user_2).count()
        followers_count = Follow.objects.filter(author=self.user_1).count()

        self.assertEqual(following_count, 1)
        self.assertEqual(followers_count, 1)

    def test_unfollow(self):
        """Проверяем что отписка работает."""
        self.authorized_follower.get(self.PROFILE_UNFOLLOW_URL)

        following_count = Follow.objects.filter(user=self.user_2).count()
        followers_count = Follow.objects.filter(author=self.user_1).count()

        self.assertEqual(following_count, 0)
        self.assertEqual(followers_count, 0)

    def test_follow_index(self):
        """Проверяем follow index."""
        self.authorized_follower.get(reverse(
            'profile_follow',
            kwargs={'username': self.user_1.username}))

        response = self.authorized_follower.get(self.FOLLOW_URL)
        object = response.context['page'][0]
        expected_text = object.text
        self.assertEqual(expected_text, self.post.text)

        response = self.authorized_unfollower.get(self.FOLLOW_URL)
        assert not response.context['page'].has_next()
