# Import Django admin module and all models from the current app
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Product, Sale, SaleItem, Inventory

# Custom admin site configuration
class POSAdminSite(admin.AdminSite):
    site_header = "Point of Sale Administration"
    site_title = "POS Admin Portal"
    index_title = "Welcome to POS Management System"

# Create custom admin site instance
admin_site = POSAdminSite(name='pos_admin')

# Admin configuration for Category model - manages product categories
@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('name', 'description', 'product_count', 'created_products')
    # Fields that can be searched in admin
    search_fields = ('name', 'description')
    # Fields that can be edited directly in list view
    list_editable = ('description',)
    # Ordering of list view
    ordering = ('name',)

    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = "Products"

    def created_products(self, obj):
        count = obj.product_set.count()
        url = reverse('admin:pos_app_product_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">View {} products</a>', url, count)
    created_products.short_description = "Actions"

# Admin configuration for Product model - manages product inventory
@admin.register(Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('name', 'category', 'formatted_price', 'stock_quantity', 'stock_status', 'barcode', 'updated_at')
    # Filters available in admin sidebar
    list_filter = ('category', 'stock_quantity', 'created_at', 'updated_at')
    # Fields that can be searched in admin
    search_fields = ('name', 'barcode', 'category__name')
    # Fields that can be edited directly in list view
    list_editable = ('stock_quantity',)
    # Fields that are read-only in admin forms
    readonly_fields = ('created_at', 'updated_at')
    # Ordering of list view
    ordering = ('-updated_at',)
    # Number of items per page
    list_per_page = 25

    def formatted_price(self, obj):
        return f"₱{obj.price}"
    formatted_price.short_description = "Price"
    formatted_price.admin_order_field = 'price'

    def stock_status(self, obj):
        if obj.stock_quantity == 0:
            return format_html('<span style="color: red; font-weight: bold;">Out of Stock</span>')
        elif obj.stock_quantity < 10:
            return format_html('<span style="color: orange; font-weight: bold;">Low Stock ({})</span>', obj.stock_quantity)
        else:
            return format_html('<span style="color: green;">In Stock ({})</span>', obj.stock_quantity)
    stock_status.short_description = "Stock Status"

    # Custom actions
    actions = ['mark_out_of_stock', 'increase_stock']

    def mark_out_of_stock(self, request, queryset):
        queryset.update(stock_quantity=0)
        self.message_user(request, f"{queryset.count()} products marked as out of stock.")
    mark_out_of_stock.short_description = "Mark selected products as out of stock"

    def increase_stock(self, request, queryset):
        for product in queryset:
            product.stock_quantity += 10
            product.save()
        self.message_user(request, f"Increased stock by 10 for {queryset.count()} products.")
    increase_stock.short_description = "Increase stock by 10 for selected products"

# Admin configuration for Sale model - manages sales transactions
@admin.register(Sale, site=admin_site)
class SaleAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'user', 'formatted_total', 'payment_method', 'item_count', 'created_at', 'view_items')
    # Filters available in admin sidebar
    list_filter = ('payment_method', 'created_at', 'user')
    # Fields that can be searched in admin
    search_fields = ('id', 'user__username', 'user__email')
    # Fields that are read-only in admin forms
    readonly_fields = ('created_at',)
    # Ordering of list view
    ordering = ('-created_at',)
    # Number of items per page
    list_per_page = 20

    def formatted_total(self, obj):
        return f"₱{obj.total_amount}"
    formatted_total.short_description = "Total Amount"
    formatted_total.admin_order_field = 'total_amount'

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Items"

    def view_items(self, obj):
        url = reverse('admin:pos_app_saleitem_changelist') + f'?sale__id__exact={obj.id}'
        return format_html('<a href="{}" class="button">View Items</a>', url)
    view_items.short_description = "Actions"

# Admin configuration for SaleItem model - manages individual sale items
@admin.register(SaleItem, site=admin_site)
class SaleItemAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('sale', 'product', 'quantity', 'formatted_unit_price', 'formatted_total_price', 'sale_date')
    # Filters available in admin sidebar
    list_filter = ('sale__created_at', 'product__category')
    # Fields that can be searched in admin
    search_fields = ('sale__id', 'product__name', 'product__barcode')
    # Fields that are read-only in admin forms
    readonly_fields = ('sale', 'product', 'quantity', 'unit_price', 'total_price')
    # Ordering of list view
    ordering = ('-sale__created_at',)
    # Number of items per page
    list_per_page = 25

    def formatted_unit_price(self, obj):
        return f"₱{obj.unit_price}"
    formatted_unit_price.short_description = "Unit Price"

    def formatted_total_price(self, obj):
        return f"₱{obj.total_price}"
    formatted_total_price.short_description = "Total Price"

    def sale_date(self, obj):
        return obj.sale.created_at
    sale_date.short_description = "Sale Date"
    sale_date.admin_order_field = 'sale__created_at'

# Admin configuration for Inventory model - manages inventory tracking
@admin.register(Inventory, site=admin_site)
class InventoryAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('product', 'quantity', 'last_updated', 'stock_alert')
    # Filters available in admin sidebar
    list_filter = ('last_updated',)
    # Fields that can be searched in admin
    search_fields = ('product__name', 'product__barcode')
    # Fields that are read-only in admin forms
    readonly_fields = ('last_updated',)
    # Ordering of list view
    ordering = ('-last_updated',)

    def stock_alert(self, obj):
        if obj.quantity == 0:
            return format_html('<span style="color: red;">⚠️ Critical</span>')
        elif obj.quantity < 10:
            return format_html('<span style="color: orange;">⚠️ Low</span>')
        else:
            return format_html('<span style="color: green;">✓ Normal</span>')
    stock_alert.short_description = "Alert"
