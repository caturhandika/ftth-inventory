from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Warehouse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} @ {self.warehouse.name}"

class StockRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('rejected', 'Rejected'),
    ]
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)  # Added warehouse field

    def __str__(self):
        return f"Request #{self.id} by {self.requested_by.username}"

class StockRequestItem(models.Model):
    request = models.ForeignKey(StockRequest, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    fulfilled_quantity = models.PositiveIntegerField(null=True, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)  # Added serial_number for fulfillment

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class FulfilledItemSerial(models.Model):
    stock_request_item = models.ForeignKey(
        StockRequestItem,
        on_delete=models.CASCADE,
        related_name='serials'
    )
    serial_number = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.serial_number} for {self.stock_request_item}"
