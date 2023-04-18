from django.test import TestCase, Client
from ..models import Customer
from rest_framework.reverse import reverse


class TestCustomerUpdate(TestCase):
    
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

        Customer.objects.create_user(**self.test_customer1)
        Customer.objects.create_user(**self.test_customer2)

        self.path_one = reverse(
            'customer_get_one',
            kwargs={
                'pk':Customer.objects.get(email=self.test_customer1["email"]).id
            }
        )
        self.path_all = reverse('customer_get_all')

    def test_successful_get_all(self):
        self.customer.login(email=self.test_customer1["email"], password=self.test_customer1["password"])
        response = self.customer.get(
            self.path_all,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(Customer.objects.all()))

    def test_successfult_get_self(self):
        self.customer.login(email=self.test_customer1["email"], password=self.test_customer1["password"])
        response = self.customer.get(
            self.path_one,
        )
        self.assertEqual(response.status_code, 200)

    def test_successfult_get_other(self):
        self.customer.login(email=self.test_customer2["email"], password=self.test_customer2["password"])
        response = self.customer.get(
            self.path_one,
        )
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_get_all(self):
        response = self.customer.get(
            self.path_all,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(Customer.objects.all()))

    def test_unauthorized_get_one(self):
        response = self.customer.get(
            self.path_one,
        )
        self.assertEqual(response.status_code, 200)

    def test_customer_doesnt_exists(self):
        self.customer.login(email=self.test_customer2["email"], password=self.test_customer2["password"])
        Customer.objects.get(email=self.test_customer1["email"]).delete()
        response = self.customer.get(
            self.path_one,
        )
        self.assertEqual(response.status_code, 404)