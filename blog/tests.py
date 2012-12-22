"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from blog.models import Post
from django.test.client import Client
from django.utils import timezone


class SimpleTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(post_name='ASDF',
           post_text='Hello world',
           pub_date=timezone.now())
        self.client = Client()

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.post.save()
        self.assertIsInstance(self.post, Post)

    def test_links(self):
        # Issue a GET request
        response = self.client.get('/blog/')
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        #print response
        # Issue a GET request
        response = self.client.get('/blog/1/')
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        #print response
