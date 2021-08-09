from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class PostURLTests(TestCase):
    """URL в рамках теста."""
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

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='testURLtitle',
            slug='testURLgroup',
            description='testURLdescription'
        )
        cls.user = User.objects.create(
            first_name='testURLname',
            last_name='testURLlastname',
            username='testURLusername',
            email='testURLemail@yandex.ru'
        )
        cls.post = Post.objects.create(
            text='testURLtext',
            author=PostURLTests.user,
            group=PostURLTests.group
        )
        cls.u_user = User.objects.create(
            first_name='u_testURLname',
            last_name='u_testURLlastname',
            username='u_testURLusername',
            email='u_testURLemail@yandex.ru'
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованые клиенты
        self.authorized_client_author = Client()
        self.authorized_client_not_author = Client()
        self.authorized_client_author.force_login(self.__class__.user)
        self.authorized_client_not_author.force_login(self.__class__.u_user)

    def test_index_guest_client(self):
        """Страница / доступна гостевому пользователю."""
        response = self.guest_client.get(self.HOMEPAGE_URL)
        self.assertEqual(response.status_code, 200)

    def test_group_guest_client(self):
        """Страница /group/testgroup/ доступна гостевому пользователю."""
        response = self.guest_client.get(self.GROUP_URL)
        self.assertEqual(response.status_code, 200)

    def test_profile_guest_client(self):
        """Страница /profile/ доступна гостевому пользователю."""
        response = self.guest_client.get(self.PROFILE_URL)
        self.assertEqual(response.status_code, 200)

    def test_profile_post_id_guest_client(self):
        """Страница /profile/post_id/ доступна гостевому пользователю."""
        response = self.guest_client.get(self.PROFILE_URL)
        self.assertEqual(response.status_code, 200)

    def test_new_authorized_client(self):
        """Страница /new/ доступна авторизованному пользователю."""
        response = self.authorized_client_author.get(self.NEWPOST_URL)
        self.assertEqual(response.status_code, 200)

    def test_new_guest_client(self):
        """Страница /new/ доступна гостевому пользователю."""
        response = self.guest_client.get(self.NEWPOST_URL)
        self.assertEqual(response.status_code, 302)

    def test_profile_post_id_edit_access_anonymous(self):
        """Страница /testURLusername/1/edit/ перенаправляет
        гостевого пользователя.
        """
        response = self.guest_client.get(self.POSTEDIT_URL)
        self.assertEqual(response.status_code, 302)

    def test_profile_post_id_edit_access_author(self):
        """Страница /testURLusername/1/edit/ доступна
        для автора.
        """
        response = self.authorized_client_author.get(self.POSTEDIT_URL)
        self.assertEqual(response.status_code, 200)

    def test_profile_post_id_edit_access_not_author(self):
        """Страница /testURLusername/1/edit/ перенаправляет
        не автора.
        """
        response = self.authorized_client_not_author.get(self.POSTEDIT_URL)
        self.assertEqual(response.status_code, 302)

    def test_new_redirect_anonymous_on_login(self):
        """Страница /new/ перенаправит анонимного пользователя
        на страницу логина.
        """
        response = self.guest_client.get(self.NEWPOST_URL, follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/new/')

    def test_edit_redirect_anonymous_on_login(self):
        """Страница /testURLusername/1/edit/ перенаправит
        анонимного пользователя на страницу логина.
        """
        response = self.guest_client.get(self.POSTEDIT_URL, follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/testURLusername/1/edit/')

    def test_edit_redirect_authorized_client_not_author_on_post(self):
        """Страница /testURLusername/1/edit/ перенаправит
        пользователя, но не автора на страницу логина.
        """
        response = self.authorized_client_not_author.get(
            self.POSTEDIT_URL,
            follow=True
        )
        self.assertRedirects(
            response, self.POST_URL)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            self.HOMEPAGE_URL: 'posts/index.html',
            self.PROFILE_URL: 'posts/profile.html',
            self.POST_URL: 'posts/post.html',
            self.POSTEDIT_URL: 'posts/new.html',
            self.NEWPOST_URL: 'posts/new.html',
            self.GROUP_URL: 'posts/group.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client_author.get(adress)
                self.assertTemplateUsed(response, template)
