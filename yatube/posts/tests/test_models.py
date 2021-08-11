from django.test import TestCase
from posts.models import Group, Post, User


class PostModelTest(TestCase):
    """URL/Записи в рамках теста."""
    TEST_TEXT = 'testMODELtext'
    TEST_USER = 'testMODELuser'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Создаём тестовую запись в БД."""
        cls.user = User.objects.create_user(PostModelTest.TEST_USER)
        cls.post = Post.objects.create(
            text=PostModelTest.TEST_TEXT,
            author=cls.user
        )

    def test_str(self):
        """Проверяем что у str правильный вывод."""
        post = str(PostModelTest.post)
        expected_value = PostModelTest.TEST_TEXT[:15]
        self.assertEqual(
            post,
            expected_value)


class GroupModelTest(TestCase):
    """URL/Записи в рамках теста."""
    TEST_TITLE = 'testMODELtitle'
    TEST_SLUG = 'test_group'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Создаём тестовую запись в БД."""
        cls.group = Group.objects.create(
            title=GroupModelTest.TEST_TITLE,
            slug=GroupModelTest.TEST_SLUG,
        )

    def test_str(self):
        """Проверяем что у str правильный вывод."""
        group = str(GroupModelTest.group)
        expected_value = GroupModelTest.TEST_TITLE
        self.assertEqual(
            group,
            expected_value)


class CommentModelTest(TestCase):
    """URL/Записи в рамках теста."""
    TEST_TEXT = 'testMODELtext'
    TEST_USER = 'testMODELuser'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Создаём тестовую запись в БД."""
        cls.user = User.objects.create_user(CommentModelTest.TEST_USER)
        cls.comment = Post.objects.create(
            text=CommentModelTest.TEST_TEXT,
            author=cls.user
        )

    def test_str(self):
        """Проверяем что у str правильный вывод."""
        comment = str(CommentModelTest.comment)
        expected_value = CommentModelTest.TEST_TEXT[:15]
        self.assertEqual(
            comment,
            expected_value)


class FollowModelTest(TestCase):
    """URL/Записи в рамках теста."""
    TEST_USER_1 = 'testMODELuser_1'
    TEST_USER_2 = 'testMODELuser_2'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Создаём тестовую запись в БД."""
        cls.user = User.objects.create_user(FollowModelTest.TEST_USER_1)
        cls.author = User.objects.create_user(FollowModelTest.TEST_USER_2)

    def test_str(self):
        """Проверяем что у str правильный вывод."""
        user = str(FollowModelTest.user)
        expected_user = str(FollowModelTest.user)
        author = str(FollowModelTest.author)
        expected_author = str(FollowModelTest.author)
        self.assertEqual(user, expected_user)
        self.assertEqual(author, expected_author)
