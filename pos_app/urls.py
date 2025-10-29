# Import Django URL configuration module and views from current app
from django.urls import path
from . import views

# Namespace for this app's URLs to avoid conflicts with other apps
app_name = 'pos_app'

# URL patterns for the POS application
urlpatterns = [
    # Home page - accessible to all users
    path('', views.home, name='home'),
    # User registration page - accessible to all users
    path('register/', views.register, name='register'),
    # Product list page - requires login
    path('products/', views.product_list, name='product_list'),
    # Individual product detail page - requires login
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    # Sale processing page - requires login
    path('sale/', views.sale_process, name='sale_process'),
    # Add product to cart - requires login
    path('sale/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # Remove product from cart - requires login
    path('sale/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    # Clear entire cart - requires login
    path('sale/clear/', views.clear_cart, name='clear_cart'),
    # Sale confirmation page - requires login
    path('sale/confirm/', views.sale_confirm, name='sale_confirm'),
    # Sale detail page - requires login
    path('sale/<int:pk>/', views.sale_detail, name='sale_detail'),
    # Sales reports page - requires login
    path('reports/sales/', views.sales_report, name='sales_report'),
]
