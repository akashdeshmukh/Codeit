"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from codeit.models import *


class SimpleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            receipt_no=1,
            first_name="Sanket",
            last_name="Sudake",
            total_points=0,
            year="te",
        )
        self.user.save()
        self.client = Client()

    def test_objects(self):
        self.assertIsInstance(self.user, User)
        self.assertIsInstance(self.client, Client)
        self.client.get("/")
        response = self.client.post("/", {"receipt_no": self.user.receipt_no,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "year": self.user.year})
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)
