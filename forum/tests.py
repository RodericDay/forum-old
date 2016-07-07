from django.test import TestCase
from django.contrib.auth.models import User


class TestSuite(TestCase):
    fixtures = ['dump.json']

    def setUp(self):
        user = User.objects.get(username="ethan")
        self.client.force_login(user)

    def test_profile(self):
        response = self.client.get('/profile/')
        self.assertContains(response, "welcome, ethan!")

    def test_logged_out(self):
        self.client.logout()
        response = self.client.get('/profile/')
        self.assertEquals(response.status_code, 302)

    def test_topic_list_performance(self):
        with self.assertNumQueries(17):
            response = self.client.get('/topics/')
        self.assertContains(response, "gramsci")

    def test_topic_list_permissions(self):
        response = self.client.get('/topics/')
        self.assertNotContains(response, "misc pics")

    def test_topic_list_tags(self):
        response = self.client.get('/topics/?tag=economics&tag=politics')
        self.assertNotContains(response, "orwell")

    def test_quickpost(self):
        payload = {"timestamp": "2016-06-29T04:39Z"}
        payload["content"] = "boogiewoogie"
        response = self.client.post('/topics/9/ajax/', payload)
        payload["content"] = "fengshui"
        response = self.client.post('/topics/9/ajax/', payload)
        self.assertContains(response, "boogiewoogie")
        self.assertContains(response, "fengshui")
