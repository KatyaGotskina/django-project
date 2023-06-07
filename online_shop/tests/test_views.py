from django.test import TestCase
from django.urls import reverse
from rest_framework.status import HTTP_200_OK as OK
from shop_app.models import Users


def create_view_tests(url, page_name, template):
    class ViewTest(TestCase):

        def setUp(self):
            self.user = Users.objects.create_user(username='test', password='test')
            self.client.force_login(user=self.user)
            
           

        def test_view_exists_at_url(self):
            self.assertEqual(self.client.get(url).status_code, OK)

        def test_view_exists_by_name(self):
            self.assertEqual(self.client.get(reverse(page_name)).status_code, OK)

        def test_view_uses_template(self):
            resp = self.client.get(reverse(page_name))
            self.assertEqual(resp.status_code, OK)
            self.assertTemplateUsed(resp, template)

    return ViewTest


book_attrs = {'title': 'Book', 'volume': 10}
genre_attrs = {'name': 'genre'}
author_attrs = {'full_name': 'The Fool Name'}

MenuViewTests = create_view_tests('/menu/', 'menu', 'shop_app/menu.html')
MainViewTests = create_view_tests('', 'home', 'shop_app/homepage.html')
ProfileViewTests = create_view_tests('/profile/', 'profile', 'shop_app/profile.html')