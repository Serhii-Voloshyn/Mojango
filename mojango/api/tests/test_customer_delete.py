from django.test import TestCase, Client
from ..models import Customer
from rest_framework.reverse import reverse


class TestCustomerDelete(TestCase):
    
    def setUp(self):
        self.customer = Client()

        self.test_customer1 = {
            'email': 'ser1@gmail.com',
            'password': 'abras1234',
            'first_name': 'ser',
            'last_name': 'ser'
        }
        self.test_customer2 = {
            'email': 'ser2@gmail.com',
            'password': 'abras1234',
            'first_name': 'ser',
            'last_name': 'ser'
        }
        self.superuser = {
            'email': 'ser@gmail.com',
            'password': 'abras1234',
            'first_name': 'ser',
            'last_name': 'ser'
        }
        
        Customer.objects.create_user(**self.test_customer1)
        Customer.objects.create_user(**self.test_customer2)
        Customer.objects.create_superuser(**self.superuser)

        self.path = reverse(
            'customer_delete',
            kwargs={
                'pk':Customer.objects.get(email=self.test_customer1["email"]).id
            }
        )
        
    def test_successful_delete_by_customer(self):
        self.customer.login(email=self.test_customer1["email"], password=self.test_customer1["password"])
        response = self.customer.delete(
            self.path
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Customer.objects.all()), 3)
        self.assertEqual(Customer.objects.get(email=self.test_customer1["email"]).is_active, False)

    def test_successful_delete_by_admin(self):
        self.customer.login(email=self.superuser["email"], password=self.superuser["password"])
        response = self.customer.delete(
            self.path
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Customer.objects.all()), 3)
        self.assertEqual(Customer.objects.get(email=self.test_customer1["email"]).is_active, False)

    def test_other_customer_delete_attempt(self):
        self.customer.login(email=self.test_customer2["email"], password=self.test_customer2["password"])
        response = self.customer.delete(
            self.path
        )
        self.assertEqual(response.status_code, 405)
        self.assertEqual(len(Customer.objects.all()), 3)
        self.assertEqual(Customer.objects.get(email=self.test_customer1["email"]).is_active, True)

    def test_unauthorized_delete_attempt(self):

        response = self.customer.delete(
            self.path
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(Customer.objects.all()), 3)
        self.assertEqual(Customer.objects.get(email=self.test_customer1["email"]).is_active, True)
