from django.urls import reverse
from django.test import TestCase


class AccountsTests(TestCase):

    def test_login_page(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_functionality(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'user',
            'password': 'pass',
        })
        # ... інші перевірки

    def test_logout(self):
        response = self.client.get(reverse('accounts:logout'))
        # ... інші перевірки

    def test_register_page(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_functionality(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'password123',
        })
        # ... інші перевірки
