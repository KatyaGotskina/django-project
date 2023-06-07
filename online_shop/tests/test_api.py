from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from shop_app.models import Categories, Products, Users


def create_api_testcase(path, model_class, data):
    class CustomApiTestCase(APITestCase):
        def setUp(self) -> None:
            universal_args = {'password': 'test',
                              'first_name': 'test', 'last_name': 'testik'}
            self.user = Users.objects.create_user(
                username='testuser', **universal_args)
            self.admin = Users.objects.create_user(
                username='admin', email='test@gmail.com', is_superuser=True, **universal_args)
            self.user_token = Token.objects.create(user=self.user)
            self.admin_token = Token.objects.create(user=self.admin)

        def user_auth(self):
            self.client.credentials(
                HTTP_AUTORIZATION='Token ' + self.user_token.key)
            self.client.force_authenticate(self.user)

        def admin_auth(self):
            self.client.force_authenticate(self.admin)
            self.client.credentials(
                HTTP_AUTORIZATION='Token ' + self.admin_token.key)

        def test_get(self):
            response = self.client.get(path)
            self.assertEqual(response.status_code,
                             status.HTTP_401_UNAUTHORIZED)
            self.client.force_authenticate(self.user)
            response = self.client.get(path)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_post(self):
            self.client.credentials(
                HTTP_AUTORIZATION='Token ' + self.user_token.key)
            self.assertEqual(self.client.post(
                path, data).status_code, status.HTTP_401_UNAUTHORIZED)
            self.client.force_authenticate(self.user)
            self.assertEqual(self.client.post(
                path, data).status_code, status.HTTP_403_FORBIDDEN)
            self.client.logout()
            self.admin_auth()
            self.assertEqual(self.client.post(
                path, data).status_code, status.HTTP_201_CREATED)

        def test_delete(self):
            self.admin_auth()
            obj = model_class.objects.create(**data)
            self.assertEqual(self.client.delete(
                f'{path}{str(obj.id)}/').status_code, status.HTTP_204_NO_CONTENT)
            self.client.logout()
            self.user_auth()
            obj = model_class.objects.create(**data)
            self.assertEqual(self.client.delete(
                f'{path}{str(obj.id)}/').status_code, status.HTTP_403_FORBIDDEN)

        def test_update(self):
            self.admin_auth()
            obj = model_class.objects.create(**data)
            data['name'] = 'test2'
            self.assertEqual(self.client.put(
                f'{path}{str(obj.id)}/', data).status_code, status.HTTP_200_OK)
            self.client.logout()
            self.user_auth()
            obj = model_class.objects.create(**data)
            self.assertEqual(self.client.put(
                f'{path}{str(obj.id)}/', data).status_code, status.HTTP_403_FORBIDDEN)

    return CustomApiTestCase


CategoryApiTestCase = create_api_testcase(
    '/rest/category/', Categories,  data={'name': 'test'})
ProductApiTestCase = create_api_testcase('/rest/product/', Products, data={
    "name": "test",
            "price": 20,
            "number": 43,
            "status": "for sale"
})
