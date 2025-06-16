from django.test import TestCase
from django.urls import reverse
from .models import Review, Product, Category


class MainViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            name='Test Product',
            short_description='Short desc',
            full_description='Full desc',
            price=100.00,
            image='products/test.jpg',
            category=self.category
        )
        self.review = Review.objects.create(
            name="Test User", message="Good product!", rating=5)

    def test_home_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('sliders', response.context)
        self.assertIn('reviews', response.context)
        self.assertIn('popular_products', response.context)
        self.assertIn('recent_news', response.context)

    def test_product_list_view(self):
        url = reverse('product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('products', response.context)
        self.assertIn('categories', response.context)

    def test_product_detail_view(self):
        url = reverse('product_detail', args=[self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], self.product)

    def test_contact_view_get(self):
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_contact_view_post_valid(self):
        url = reverse('contact')
        data = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'message': 'Hello!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])
