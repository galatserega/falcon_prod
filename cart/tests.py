from django.test import TestCase, Client
from django.urls import reverse
from main.models import Product, Category


class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Test Category", slug="test-category")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            slug="test-product",
            price=10.00,
            full_description="Test description"
        )

    def test_add_to_cart(self):
        response = self.client.get(
            reverse("cart:cart_add", args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # should redirect
        session = self.client.session
        cart = session.get("cart", {})
        self.assertIn(str(self.product.id), cart)

    def test_remove_from_cart(self):
        session = self.client.session
        session["cart"] = {str(self.product.id): {"quantity": 1}}
        session.save()
        response = self.client.get(
            reverse("cart:cart_remove", args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        cart = session.get("cart", {})
        self.assertNotIn(str(self.product.id), cart)

    def test_cart_detail(self):
        response = self.client.get(reverse("cart:cart_detail"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/cart_detail.html")
