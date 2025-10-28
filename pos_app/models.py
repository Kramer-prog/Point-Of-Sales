# Import necessary Django modules for database models and user authentication
from django.db import models
from django.contrib.auth.models import User

# Model representing product categories in the POS system
class Category(models.Model):
    # Name of the category (e.g., "Electronics", "Clothing") - must be unique
    name = models.CharField(max_length=100, unique=True)
    # Optional description of the category
    description = models.TextField(blank=True)

    # String representation of the category object
    def __str__(self):
        return self.name

# Model representing products available for sale
class Product(models.Model):
    # Name of the product
    name = models.CharField(max_length=200)
    # Foreign key linking to Category - when category is deleted, products are deleted too
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Selling price of the product
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Cost price for profit calculation (default 0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Current stock quantity
    stock_quantity = models.PositiveIntegerField(default=0)
    # Optional unique barcode for product identification
    barcode = models.CharField(max_length=100, unique=True, blank=True)
    # Optional detailed description
    description = models.TextField(blank=True)
    # Timestamp when product was created (auto-set)
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp when product was last updated (auto-set)
    updated_at = models.DateTimeField(auto_now=True)

    # String representation of the product object
    def __str__(self):
        return self.name

# Model representing sales transactions
class Sale(models.Model):
    # User who processed the sale
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Total amount of the sale
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Payment method choices for the sale
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('other', 'Other')
    ], default='cash')
    # Timestamp when sale was created (auto-set)
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation of the sale object
    def __str__(self):
        return f"Sale #{self.id} - {self.total_amount}"

# Model representing individual items within a sale
class SaleItem(models.Model):
    # Foreign key to the Sale this item belongs to
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    # Foreign key to the Product being sold
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Quantity of this product in the sale
    quantity = models.PositiveIntegerField()
    # Price per unit at the time of sale
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Total price for this item (quantity * unit_price)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # String representation of the sale item
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

# Model for tracking inventory levels (one-to-one with Product)
class Inventory(models.Model):
    # One-to-one relationship with Product - each product has one inventory record
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    # Current inventory quantity
    quantity = models.PositiveIntegerField(default=0)
    # Timestamp of last inventory update (auto-set)
    last_updated = models.DateTimeField(auto_now=True)

    # String representation of the inventory record
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
