from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class ClothType(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (₦{self.price})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('RECEIVED', 'Received'),
        ('WASHING', 'Washing'),
        ('READY', 'Ready'),
        ('COMPLETED', 'Completed'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_code = models.CharField(max_length=50, unique=True, blank=True)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    payment_receipt = models.ImageField(upload_to="payment_receipts/", null=True, blank=True)
    is_payment_approved = models.BooleanField(default=False)
    receipt_pdf = models.FileField(upload_to="invoices/", null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expected_delivery = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.order_code} - {self.customer.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.order_code:
            last_id = Order.objects.count() + 1
            formatted_date = self.created_at.strftime('%Y%m%d')
            self.order_code = f"INV-{formatted_date}-{last_id:05d}"

            super().save(update_fields=['order_code'])

    def calculate_total(self):
        total = sum(item.subtotal() for item in self.items.all())
        self.total_amount = total
        self.save()
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    cloth_type = models.ForeignKey(ClothType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.calculate_total()
