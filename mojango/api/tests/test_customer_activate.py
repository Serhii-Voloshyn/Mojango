from django.test import TestCase, Client
from ..models import Customer
from rest_framework.reverse import reverse


class TestCustomerActivate(TestCase):
    
    def setUp(self):
        self.customer = Client()

        self.test_customer = {
            'email': 'ser@gmail.com',
            'password': 'abras1234',
            'first_name': 'ser',
            'last_name': 'ser'
        }
        self.path = reverse('customer_create')
        Customer.objects.create_user(**self.test_customer)
        
    def test_successful_receive_email(self):
        data = {
            'email': 'ser1@gmail.com',
            'password': 'abras1234',
            'first_name': 'ser',
            'last_name': 'ser'
        }
        response = self.customer.post(
            path=self.path,
            data=data,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Customer.objects.all()), 2)
        self.assertNotEqual(Customer.objects.get(email=data['email']).password, data['password'])

    def test_short_password(self):
        data = {
            'email': 'ser1@gmail.com',
            'password': 'abras',
            'first_name': 'ser',
            'last_name': 'ser'
        }
        response = self.customer.post(
            path=self.path,
            data=data,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Customer.objects.all()), 1)

    def test_email_exists(self):
        data = {
            'email': self.test_customer['email'],
            'password': 'abras1234',
            'first_name': 'ser',
            'last_name': 'ser'
        }
        response = self.customer.post(
            path=self.path,
            data=data,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Customer.objects.all()), 1)

    def test_empty_full_name(self):
        data = {
            'email': 'ser1@gmail.com',
            'password': 'abras1234',
            'first_name': '',
            'last_name': ''
        }
        response = self.customer.post(
            path=self.path,
            data=data,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Customer.objects.all()), 1)
