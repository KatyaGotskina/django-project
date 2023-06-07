from django.test import TestCase
from shop_app import forms
from random import sample
from string import ascii_letters


def random_string(size: int = 10):
    return ''.join(sample(ascii_letters, size))



class WeatherFormTests(TestCase):

    def test_unsuccessful(self):
        self.assertFalse(forms.RegistrationForm(data={'username': 'test'}).is_valid())