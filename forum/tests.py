from django.test import TestCase

from django.contrib.auth.models import User


class TestSuite(TestCase):

    def setUp(self):
        user = User.objects.create(username="Anne")
        self.client.force_login(user)

    def test_logged_out(self):
        self.client.logout()
        response = self.client.get('/profile/')
        self.assertEquals(response.status_code, 302)

    def test_profile(self):
        response = self.client.get('/profile/')
        self.assertContains(response, "welcome, Anne!")
