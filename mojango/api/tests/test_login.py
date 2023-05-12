from django.test import TestCase, Client
from ..models import Customer
from rest_framework.reverse import reverse


class TestLogin(TestCase):
    
    def setUp(self):
        self.customer = Client()

        self.test_customer = {
            'email': 'ser@gmail.com',
            'password': 'abras1234',
            'first_name': 'ser',
            'last_name': 'ser'
        }
        self.path = reverse('login')
        self.token_varify = reverse('token_verify')
        self.token_refresh = reverse('token_refresh')

        Customer.objects.create_user(**self.test_customer)
        
    def test_successful_login(self):
        data = {
            'email': self.test_customer['email'],
            'password': self.test_customer['password'],
        }
        response = self.customer.post(
            path=self.path,
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
        self.assertIn('access', response.json()['token'])
        self.assertIn('refresh', response.json()['token'])
    
    def test_successful_jwt_tokens(self):
        data = {
            'email': self.test_customer['email'],
            'password': self.test_customer['password'],
        }
        response = self.customer.post(
            path=self.path,
            data=data,
        )
        access = {'token': response.json()['token']['access']}
        refresh = {'refresh': response.json()['token']['refresh']}

        response = self.customer.post(
            path=self.token_varify,
            data=access
        )
        self.assertEqual(response.status_code, 200)

        response = self.customer.post(
            path=self.token_refresh,
            data=refresh
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())

    def test_invalid_jwt_tokens(self):
        data = {
            'email': self.test_customer['email'],
            'password': self.test_customer['password'],
        }
        response = self.customer.post(
            path=self.path,
            data=data,
        )
        access = {'token': response.json()['token']['access'][:-1]}
        refresh = {'refresh': response.json()['token']['refresh'][:-1]}

        response = self.customer.post(
            path=self.token_varify,
            data=access
        )
        self.assertEqual(response.status_code, 401)

        response = self.customer.post(
            path=self.token_refresh,
            data=refresh
        )
        self.assertEqual(response.status_code, 401)
        self.assertNotIn('access', response.json())

    def test_invald_password_login(self):
        data = {
            'email': self.test_customer['email'],
            'password': self.test_customer['password'] + '1',
        }
        response = self.customer.post(
            path=self.path,
            data=data,
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn('token', response.json())

    def test_successful_get(self):
        self.customer.login(email=self.test_customer['email'], password=self.test_customer['password'])
        response = self.customer.get(
            path=self.path,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.json())
        self.assertIn('auth', response.json())

    def test_unauthorized_get(self):
        response = self.customer.get(
            path=self.path,
        )
        self.assertEqual(response.status_code, 401)
        self.assertNotIn('user', response.json())
        self.assertNotIn('auth', response.json())