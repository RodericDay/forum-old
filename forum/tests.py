from django.test import TestCase

from django.contrib.auth.models import User


class TestSuite(TestCase):

    def test_home(self):
        user = User.objects.create(username="Anne")
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertContains(response, "welcome, Anne!")
        self.assertContains(response, "avatars/default.jpg")
