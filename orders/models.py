from django.db import models
from main.models import Product
# Create your models here.

class Order(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Замовлення №{self.id} — {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.price * self.quantity
