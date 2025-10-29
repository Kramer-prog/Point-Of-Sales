# Import Django admin module and all models from the current app
from django.contrib import admin
from django.db.models import Sum, Count
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Product, Sale, SaleItem, Inventory

# Inline admin for SaleItem to show items within Sale admin
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ('total_price',)
    fields = ('product', 'quantity', 'unit_price', 'total_price')

# Admin configuration for Category model - manages product categories
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('name', 'description', 'product_count', 'total_value')
    # Fields that can be searched in admin
    search_fields = ('name', 'description')

    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Products'

    def total_value(self, obj):
        total = obj.product_set.aggregate(
            total=Sum('price') * Sum('stock_quantity')
        )['total'] or 0
        return f"₱{total:.2f}"
    total_value.short_description = 'Total Value'

# Admin configuration for Product model - manages product inventory
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('name', 'category', 'price', 'stock_quantity', 'stock_status', 'barcode', 'updated_at')
    # Filters available in admin sidebar
    list_filter = ('category', 'stock_quantity', 'updated_at')
    # Fields that can be searched in admin
    search_fields = ('name', 'barcode', 'category__name')
    # Fields that are read-only in admin forms
    readonly_fields = ('created_at', 'updated_at')
    # Ordering
    ordering = ('-updated_at',)
    # Actions
    actions = ['mark_out_of_stock', 'update_stock']

    def stock_status(self, obj):
        if obj.stock_quantity == 0:
            return format_html('<span style="color: red;">Out of Stock</span>')
        elif obj.stock_quantity < 10:
            return format_html('<span style="color: orange;">Low Stock ({})</span>', obj.stock_quantity)
        else:
            return format_html('<span style="color: green;">In Stock ({})</span>', obj.stock_quantity)
    stock_status.short_description = 'Stock Status'

    def mark_out_of_stock(self, request, queryset):
        queryset.update(stock_quantity=0)
        self.message_user(request, f"Marked {queryset.count()} products as out of stock.")
    mark_out_of_stock.short_description = "Mark selected products as out of stock"

    def update_stock(self, request, queryset):
        # This would typically open a form, but for simplicity we'll just show a message
        self.message_user(request, "Use the change form to update stock quantities individually.")
    update_stock.short_description = "Update stock (use change form)"

# Admin configuration for Sale model - manages sales transactions
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'user', 'total_amount', 'payment_method', 'item_count', 'created_at', 'view_details')
    # Filters available in admin sidebar
    list_filter = ('payment_method', 'created_at', 'user')
    # Fields that can be searched in admin
    search_fields = ('id', 'user__username')
    # Fields that are read-only in admin forms
    readonly_fields = ('created_at', 'total_amount')
    # Inlines
    inlines = [SaleItemInline]
    # Actions
    actions = ['export_sales_data']

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'

    def view_details(self, obj):
        return format_html('<a href="{}" class="button">View Details</a>',
                          reverse('admin:pos_app_sale_change', args=(obj.pk,)))
    view_details.short_description = 'Details'

    def export_sales_data(self, request, queryset):
        # This would typically export to CSV/Excel, but for now just show message
        self.message_user(request, f"Exported {queryset.count()} sales records.")
    export_sales_data.short_description = "Export selected sales data"

# Admin configuration for SaleItem model - manages individual sale items
@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('sale_link', 'product', 'quantity', 'unit_price', 'total_price', 'sale_date')
    # Filters available in admin sidebar
    list_filter = ('sale__created_at', 'product__category')
    # Fields that can be searched in admin
    search_fields = ('product__name', 'sale__id')
    # Fields that are read-only in admin forms
    readonly_fields = ('total_price',)

    def sale_link(self, obj):
        return format_html('<a href="{}">Sale #{}</a>',
                          reverse('admin:pos_app_sale_change', args=(obj.sale.pk,)),
                          obj.sale.id)
    sale_link.short_description = 'Sale'

    def sale_date(self, obj):
        return obj.sale.created_at
    sale_date.short_description = 'Sale Date'
    sale_date.admin_order_field = 'sale__created_at'

# Admin configuration for Inventory model - manages inventory tracking
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('product', 'quantity', 'stock_level', 'last_updated')
    # Filters available in admin sidebar
    list_filter = ('last_updated',)
    # Fields that can be searched in admin
    search_fields = ('product__name',)
    # Fields that are read-only in admin forms
    readonly_fields = ('last_updated',)

    def stock_level(self, obj):
        if obj.quantity == 0:
            return format_html('<span style="color: red;">Critical</span>')
        elif obj.quantity < 5:
            return format_html('<span style="color: orange;">Low</span>')
        elif obj.quantity < 20:
            return format_html('<span style="color: blue;">Medium</span>')
        else:
            return format_html('<span style="color: green;">High</span>')
    stock_level.short_description = 'Stock Level'

# Custom admin site configuration
class POSAdminSite(admin.AdminSite):
    site_header = "POS System Administration"
    site_title = "POS Admin"
    index_title = "Welcome to POS System Admin"

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # Add custom ordering and grouping
        for app in app_list:
            if app['app_label'] == 'pos_app':
                app['models'].sort(key=lambda x: ['Category', 'Product', 'Inventory', 'Sale', 'SaleItem'].index(x['object_name']))
        return app_list

# Register the custom admin site
admin_site = POSAdminSite(name='pos_admin')
admin_site.register(Category, CategoryAdmin)
admin_site.register(Product, ProductAdmin)
admin_site.register(Sale, SaleAdmin)
admin_site.register(SaleItem, SaleItemAdmin)
admin_site.register(Inventory, InventoryAdmin)
