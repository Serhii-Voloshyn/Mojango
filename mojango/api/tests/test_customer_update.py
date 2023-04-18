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
            'customer_update',
            kwargs={
                'pk':Customer.objects.get(email=self.test_customer1["email"]).id
            }
        )

    def test_successful_update_by_customer(self):
        self.customer.login(email=self.test_customer1["email"], password=self.test_customer1["password"])
        response = self.customer.put(
            self.path,
            data={
                "first_name":self.test_customer1["first_name"] + "k",
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Customer.objects.get(email=self.test_customer1["email"]).first_name,
            self.test_customer1["first_name"] + "k"
        )

    def test_successful_update_password(self):
        self.customer.login(email=self.test_customer1["email"], password=self.test_customer1["password"])

        old_password = Customer.objects.get(email=self.test_customer1["email"]).password
        response = self.customer.put(
            self.path,
            data={
                "password":self.test_customer1["password"] + "k",
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(
            Customer.objects.get(email=self.test_customer1["email"]).password,
            old_password
        )
        self.assertNotEqual(
            Customer.objects.get(email=self.test_customer1["email"]).password,
            self.test_customer1["password"] + "k"
        )

    def test_unauthorized_update_attempt(self):
        response = self.customer.put(
            self.path,
            data={
                "first_name":self.test_customer1["first_name"] + "k"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(
            Customer.objects.get(email=self.test_customer1["email"]).first_name,
            self.test_customer1["first_name"] + "k"
        )

    def test_other_customer_update_attempt(self):
        self.customer.login(email=self.test_customer2["email"], password=self.test_customer2["password"])
        response = self.customer.put(
            self.path,
            data={
                "first_name":self.test_customer1["first_name"] + "k"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 405)
        self.assertNotEqual(
            Customer.objects.get(email=self.test_customer1["email"]).first_name,
            self.test_customer1["first_name"] + "k"
        )

    def test_admin_update_attempt(self):
        self.customer.login(email=self.superuser["email"], password=self.superuser["password"])
        response = self.customer.put(
            self.path,
            data={
                "first_name":self.test_customer1["first_name"] + "k"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 405)
        self.assertNotEqual(
            Customer.objects.get(email=self.test_customer1["email"]).first_name,
            self.test_customer1["first_name"] + "k"
        )
