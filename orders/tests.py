from django.urls import reverse
from main.models import Product
from django.test import TestCase


class OrderCreateViewTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test product",
            price=100.00,
            short_description="Short desc",
            full_description="Full desc",
            image="products/test.jpg"
        )
        self.url = reverse('orders:order_create')

    def test_order_create_view_get(self):
        session = self.client.session
        session['cart'] = {
            str(self.product.id): {
                'quantity': 1,
                'price': str(self.product.price)
            }
        }
        session.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
