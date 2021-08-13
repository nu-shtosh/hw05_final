from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User


class PostURLTests(TestCase):
    """URL/Записи в рамках теста."""
    HOMEPAGE_URL = reverse('index')
    GROUP_URL = reverse('group_posts', kwargs={'slug': 'testURLgroup'})
    PROFILE_URL = reverse('profile', kwargs={'username': 'testURLusername'})
    NEWPOST_URL = reverse('new_post')
    POSTEDIT_URL = reverse('post_edit', kwargs={
                           'username': 'testURLusername',
                           'post_id': '1'})
    POST_URL = reverse('post', kwargs={
                       'username': 'testURLusername',
                       'post_id': '1'})
    LOGIN_URL = reverse('login')
    TEST_TITLE = 'testURLtitle'
    TEST_SLUG = 'testURLgroup'
    TEST_TEXT = 'testURLtext'
    TEST_USER_1 = 'testURLusername'
    TEST_USER_2 = 'u_testURLusername'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title=PostURLTests.TEST_TITLE,
            slug=PostURLTests.TEST_SLUG,
        )
        cls.user = User.objects.create(
            username=PostURLTests.TEST_USER_1
        )
        cls.post = Post.objects.create(
            text=PostURLTests.TEST_TEXT,
            author=PostURLTests.user,
            group=PostURLTests.group
        )
        cls.u_user = User.objects.create(
            username=PostURLTests.TEST_USER_2
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованые клиенты
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(PostURLTests.user)
        self.authorized_client_not_author = Client()
        self.authorized_client_not_author.force_login(PostURLTests.u_user)

    def test_urls_uses_correct_template(self):
        """Проверка соответствия прямых ссылок
        и полученных через reverse(name).
        """
        templates_url_names = {
            self.HOMEPAGE_URL: 'posts/index.html',
            self.PROFILE_URL: 'posts/profile.html',
            self.POST_URL: 'posts/post.html',
            self.POSTEDIT_URL: 'posts/new.html',
            self.NEWPOST_URL: 'posts/new.html',
            self.GROUP_URL: 'posts/group.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress, template=template):
                response = self.authorized_client_author.get(adress)
                self.assertTemplateUsed(response, template)

    def test_access_client(self):
        """Тест проверки "разрешенных" url для
        авторизованных/неавторизованных юзеров.
        """
        urls_and_clients = (
            ('/', self.guest_client),
            ('/testURLusername/', self.guest_client),
            ('/testURLusername/1/', self.guest_client),
            ('/group/testURLgroup/', self.guest_client),
            ('/testURLusername/1/edit/', self.authorized_client_author),
            ('/new/', self.authorized_client_author),
        )
        for url, client in urls_and_clients:
            with self.subTest(url=url, client=client):
                response = self.authorized_client_author.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_client(self):
        """Проверка всех возможных редиректов для GET-запросов."""
        urls_and_clients = (
            ('/testURLusername/1/edit/', self.guest_client,
                self.LOGIN_URL + '/?next=/' + '/testURLusername/1/edit/'),
            ('/testURLusername/1/edit/', self.authorized_client_not_author,
                self.LOGIN_URL + '/?next=/' + 'testURLusername/1/edit/'),
            ('/new/', self.guest_client,
                self.LOGIN_URL + '/?next=/' + '/new/'),
        )
        for url, client, redirect in urls_and_clients:
            with self.subTest(url=url, client=client):
                response = self.client.get(url, follow=True)
                self.assertRedirects(response, self.LOGIN_URL + '?next=' + url)
