from django.test import TestCase

from django.contrib.auth.models import User


class TestSuite(TestCase):

    def setUp(self):
        user = User.objects.create(username="Alex")
        self.client.force_login(user)
        self.client.post('/topics/new/', {'name': "Grothendieck Primes"})

    def test_profile(self):
        response = self.client.get('/profile/')
        self.assertContains(response, "welcome, Alex!")

    def test_logged_out(self):
        self.client.logout()
        response = self.client.get('/profile/')
        self.assertEquals(response.status_code, 302)

    def test_topic_list(self):
        response = self.client.get('/topics/')
        self.assertContains(response, "Grothendieck Primes")

    def test_quickpost_and_list(self):
        response = self.client.post('/topics/1/', {'content': "57"}, follow=True)
        self.assertContains(response, "57")

    def test_post_then_list(self):
        response = self.client.post('/topics/1/new/', {'content': "57"}, follow=True)
        self.assertContains(response, "57")

    def test_edit_then_list(self):
        response = self.client.post('/posts/1/edit/', {'content': "59"}, follow=True)
        self.assertContains(response, "59")

    def test_delete_then_list(self):
        response = self.client.post('/posts/1/delete/', follow=True)
        self.assertNotContains(response, "57")
        self.assertContains(response, "deleted")
