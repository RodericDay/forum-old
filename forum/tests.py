from django.test import TestCase


class TestSuite(TestCase):

    def test_something(self):
        self.client.get('/')
