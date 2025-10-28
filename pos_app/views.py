# Import necessary Django modules and functions for views
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from .models import Product, Category, Sale, SaleItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# View for the home page - accessible to all users
def home(request):
    # Render the home template
    return render(request, 'pos_app/home.html')

# View for displaying list of products - requires user login
@login_required
def product_list(request):
    # Get all products from database
    products = Product.objects.all()
    # Render product list template with products data
    return render(request, 'pos_app/product_list.html', {'products': products})

# View for displaying individual product details - requires user login
@login_required
def product_detail(request, pk):
    # Get product by primary key or return 404 if not found
    product = get_object_or_404(Product, pk=pk)
    # Render product detail template with product data
    return render(request, 'pos_app/product_detail.html', {'product': product})

# View for processing sales transactions - requires user login
@login_required
def sale_process(request):
    # Handle POST request for completing a sale
    if request.method == 'POST':
        # Get cart from session
        cart = request.session.get('cart', {})
        # Check if cart is empty
        if not cart:
            messages.error(request, 'Cart is empty')
            return redirect('pos_app:sale_process')

        # Initialize variables for sale calculation
        total_amount = 0
        sale_items = []

        # Process each item in cart
        for product_id, quantity in cart.items():
            # Get product or return 404
            product = get_object_or_404(Product, pk=product_id)
            # Check stock availability
            if product.stock_quantity < quantity:
                messages.error(request, f'Insufficient stock for {product.name}')
                return redirect('pos_app:sale_process')
            # Calculate prices
            unit_price = product.price
            total_price = unit_price * quantity
            total_amount += total_price
            # Add item to sale items list
            sale_items.append({
                'product': product,
                'quantity': quantity,
                'unit_price': unit_price,
                'total_price': total_price
            })

        # Use database transaction for atomicity
        with transaction.atomic():
            # Create sale record
            sale = Sale.objects.create(
                user=request.user,
                total_amount=total_amount,
                payment_method=request.POST.get('payment_method', 'cash')
            )
            # Create sale items and update stock
            for item in sale_items:
                SaleItem.objects.create(
                    sale=sale,
                    product=item['product'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    total_price=item['total_price']
                )
                # Reduce product stock
                item['product'].stock_quantity -= item['quantity']
                item['product'].save()

        # Clear cart from session
        request.session['cart'] = {}
        # Show success message
        messages.success(request, f'Sale completed successfully! Total: ${total_amount}')
        # Redirect to sale detail page
        return redirect('pos_app:sale_detail', pk=sale.pk)

    # Handle GET request - display sale interface
    # Get all products for selection
    products = Product.objects.all()
    # Get cart from session
    cart = request.session.get('cart', {})
    # Prepare cart items for display
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    # Render sale process template with data
    return render(request, 'pos_app/sale_process.html', {
        'products': products,
        'cart_items': cart_items,
        'total': total
    })

# View for adding products to cart - requires user login
@login_required
def add_to_cart(request, product_id):
    # Get product or return 404
    product = get_object_or_404(Product, pk=product_id)
    # Get cart from session
    cart = request.session.get('cart', {})
    # Increment product quantity in cart
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    # Save cart back to session
    request.session['cart'] = cart
    # Show success message
    messages.success(request, f'{product.name} added to cart')
    # Redirect back to sale process page
    return redirect('pos_app:sale_process')

# View for removing products from cart - requires user login
@login_required
def remove_from_cart(request, product_id):
    # Get cart from session
    cart = request.session.get('cart', {})
    # Remove product from cart if it exists
    if str(product_id) in cart:
        del cart[str(product_id)]
        # Save updated cart to session
        request.session['cart'] = cart
        # Show success message
        messages.success(request, 'Item removed from cart')
    # Redirect back to sale process page
    return redirect('pos_app:sale_process')

# View for displaying sale details - requires user login
@login_required
def sale_detail(request, pk):
    # Get sale by primary key or return 404
    sale = get_object_or_404(Sale, pk=pk)
    # Render sale detail template with sale data
    return render(request, 'pos_app/sale_detail.html', {'sale': sale})

# View for displaying sales reports - requires user login
@login_required
def sales_report(request):
    # Get all sales ordered by creation date (newest first)
    sales = Sale.objects.all().order_by('-created_at')
    # Calculate total sales amount
    total_sales = sum(sale.total_amount for sale in sales)
    # Render sales report template with data
    return render(request, 'pos_app/sales_report.html', {
        'sales': sales,
        'total_sales': total_sales
    })

# View for user registration - accessible to all users
def register(request):
    # Handle POST request for user registration
    if request.method == 'POST':
        # Create form with POST data
        form = UserCreationForm(request.POST)
        # Validate form
        if form.is_valid():
            # Save new user
            user = form.save()
            # Log in the new user
            login(request, user)
            # Show success message
            messages.success(request, 'Registration successful!')
            # Redirect to home page
            return redirect('pos_app:home')
        else:
            # Show error message if form is invalid
            messages.error(request, 'Registration failed. Please check the form.')
    else:
        # Create empty form for GET request
        form = UserCreationForm()
    # Render registration template with form
    return render(request, 'pos_app/register.html', {'form': form})
