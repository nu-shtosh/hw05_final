import shutil

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post, User

TEST_DIR = 'ttestmedia'


class PostsFormsTests(TestCase):
    """URL/Записи в рамках теста."""
    HOMEPAGE_URL = reverse('index')
    NEWPOST_URL = reverse('new_post')
    TEST_TITLE = 'testtitleFORM'
    TEST_SLUG = 'testslugFORM'
    TEST_TEXT = 'testFORMtext'
    TEST_USER = 'testFORMusername'

    @classmethod
    def setUpClass(cls):
        """Создание записей в БД."""
        super().setUpClass()
        cls.group = Group.objects.create(
            title=PostsFormsTests.TEST_TITLE,
            slug=PostsFormsTests.TEST_SLUG,
        )
        cls.user = User.objects.create(
            username=PostsFormsTests.TEST_USER
        )
        cls.post = Post.objects.create(
            text=PostsFormsTests.TEST_TEXT,
            author=PostsFormsTests.user,
            group=PostsFormsTests.group
        )
        cls.form = PostForm()

    def setUp(self):
        """Создание клиентов."""
        self.authorized_client = Client()
        self.authorized_client.force_login(self.__class__.user)

    @override_settings(MEDIA_ROOT=(TEST_DIR))
    def test_new_post_form(self):
        """Проверяем что новая запись создается."""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        sametext = 'testtextform'
        form_data = {
            'text': sametext,
            'group': self.group.id,
            'image': uploaded
        }
        response = self.authorized_client.post(
            self.NEWPOST_URL,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, self.HOMEPAGE_URL)
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=sametext,
                group=self.group.id,
                image='posts/small.gif'
            ).exists()
        )

    def test_edit_post_form(self):
        """Проверяем что запись редактируется."""
        post = Post.objects.first()
        sametext = 'FORMFORMFORM'
        self.POSTEDIT_URL = reverse('post_edit', kwargs={
                                    'username': 'testFORMusername',
                                    'post_id': post.id})
        form_data = {'text': sametext, }
        self.authorized_client.post(self.POSTEDIT_URL,
                                    data=form_data,
                                    follow=True)
        self.assertEqual(Post.objects.first().text, sametext)


def tearDownModule():
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass
