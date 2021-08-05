from django.test import Client, TestCase
from django.urls import reverse


class AboutTestURL(TestCase):
    AUTHOR_URL = reverse('about:author')
    TECH_URL = reverse('about:tech')

    @classmethod
    def setUp(cls):
        """Создаем клиента."""
        cls.guest_client = Client()

    def test_about_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'about/author.html': self.AUTHOR_URL,
            'about/tech.html': self.TECH_URL,
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_about_author_guest_client(self):
        """Проверяем доступность author неавторизованному пользователю."""
        response = self.guest_client.get(self.AUTHOR_URL)
        self.assertEqual(response.status_code, 200)

    def test_about_tech_guest_client(self):
        """Проверяем доступность tech неавторизованному пользователю."""
        response = self.guest_client.get(self.TECH_URL)
        self.assertEqual(response.status_code, 200)
