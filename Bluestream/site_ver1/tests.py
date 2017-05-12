# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Person
from django.test import TestCase

def PersonTestCase(TestCase):
	def setup(self):
		Person.objects.create(name="hi",password="hi",email="a@aasda.com",role="Client",phone_number="1234567890")
		
	def test_person(self):
		hi = Person.get(email = "a@aasda.com")
		self.assertEqual(hi.name, "hi")
# Create your tests here.
