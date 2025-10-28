# Import Django admin module and all models from the current app
from django.contrib import admin
from .models import Category, Product, Sale, SaleItem, Inventory

# Admin configuration for Category model - manages product categories
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('name', 'description')
    # Fields that can be searched in admin
    search_fields = ('name',)

# Admin configuration for Product model - manages product inventory
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('name', 'category', 'price', 'stock_quantity', 'barcode')
    # Filters available in admin sidebar
    list_filter = ('category',)
    # Fields that can be searched in admin
    search_fields = ('name', 'barcode')
    # Fields that are read-only in admin forms
    readonly_fields = ('created_at', 'updated_at')

# Admin configuration for Sale model - manages sales transactions
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'user', 'total_amount', 'payment_method', 'created_at')
    # Filters available in admin sidebar
    list_filter = ('payment_method', 'created_at')
    # Fields that are read-only in admin forms
    readonly_fields = ('created_at',)

# Admin configuration for SaleItem model - manages individual sale items
@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('sale', 'product', 'quantity', 'unit_price', 'total_price')
    # Filters available in admin sidebar
    list_filter = ('sale',)

# Admin configuration for Inventory model - manages inventory tracking
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('product', 'quantity', 'last_updated')
    # Fields that are read-only in admin forms
    readonly_fields = ('last_updated',)
