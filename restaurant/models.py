from django.db import models
import datetime

class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('burger', 'Burger'),
        ('pizza', 'Pizza'),
        ('pasta', 'Pasta'),
        ('sweet', 'Sweet'),
        ('drink', 'Drink'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='burger')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(default='No description available')  # Added default


class CartItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True)
    items = models.ManyToManyField(MenuItem)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Add this if you want last modified
    STATUS_CHOICES = [
        ('received', 'Order Received'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('delivered', 'Delivered'),
         ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
    ]

    customer_name = models.CharField(max_length=100, default="Unknown Customer")
    order_items = models.TextField(default="No items")  # Set a default value here
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Default for existing rows
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

class ReturnRequest(models.Model):
    RETURN_STATUS = [
        ('requested', 'Return Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    return_reason = models.TextField()
    status = models.CharField(max_length=20, choices=RETURN_STATUS, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolution_notes = models.TextField(blank=True)

class CustomerContact(models.Model):
    CONTACT_TYPES = [
        ('general', 'General Inquiry'),
        ('return', 'Return Request'),
        ('complaint', 'Complaint'),
        ('compliment', 'Compliment'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True)
    resolved = models.BooleanField(default=False)

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('credit', 'Credit Card'),
        ('debit', 'Debit Card'),
        ('cash', 'Cash'),
        ('online', 'Online Payment'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)