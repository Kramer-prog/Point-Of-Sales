# Import necessary Django modules and functions for views
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction, models
from django.http import JsonResponse
from django.urls import reverse
from .models import Product, Category, Sale, SaleItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# View for the home page - accessible to all users
def home(request):
    # Get statistics for the dashboard
    products = Product.objects.all()
    categories = Category.objects.all()
    sales = Sale.objects.all()
    total_sales = sum(sale.total_amount for sale in sales)

    # Render the home template with statistics
    return render(request, 'pos_app/home.html', {
        'products': products,
        'categories': categories,
        'sales': sales,
        'total_sales': total_sales
    })

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
        # Check if this is a confirmation request
        if 'confirm_sale' in request.POST:
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
            messages.success(request, f'Sale completed successfully! Total: ₱{total_amount}')
            # Redirect to sale detail page
            return redirect('pos_app:sale_detail', pk=sale.pk)
        elif 'show_confirmation' in request.POST:
            # Show confirmation page
            return redirect('pos_app:sale_confirm')

    # Handle GET request - display sale interface
    # Get category and search query from GET parameters
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '').strip()

    # Filter products based on category and search
    products = Product.objects.all()
    if category_id and category_id != 'None' and category_id.isdigit():
        products = products.filter(category_id=int(category_id))
    if search_query:
        products = products.filter(
            models.Q(name__icontains=search_query) | models.Q(barcode__icontains=search_query)
        )

    # Get all categories for dropdown
    categories = Category.objects.all()

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
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
        'cart_items': cart_items,
        'total': total
    })

# View for adding products to cart - requires user login
@login_required
def add_to_cart(request, product_id):
    # Check if this is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Get product or return 404
        product = get_object_or_404(Product, pk=product_id)
        # Get cart from session
        cart = request.session.get('cart', {})
        # Increment product quantity in cart
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        # Save cart back to session
        request.session['cart'] = cart
        # Return JSON response for AJAX
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart',
            'cart_count': len(cart)
        })
    else:
        # Fallback for non-AJAX requests
        # Get product or return 404
        product = get_object_or_404(Product, pk=product_id)
        # Get cart from session
        cart = request.session.get('cart', {})
        # Increment product quantity in cart
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        # Save cart back to session
        request.session['cart'] = cart
        # Redirect back to sale process page with current filters and item_added parameter for toast
        category = request.GET.get('category', '')
        search = request.GET.get('search', '')
        base_url = reverse('pos_app:sale_process')
        params = []
        if category:
            params.append(f'category={category}')
        if search:
            params.append(f'search={search}')
        params.append(f'item_added={product.name}')
        query_string = '?' + '&'.join(params) if params else ''
        return redirect(base_url + query_string)

# View for removing products from cart - requires user login
@login_required
def remove_from_cart(request, product_id):
    # Check if this is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Get cart from session
        cart = request.session.get('cart', {})
        # Remove product from cart if it exists
        if str(product_id) in cart:
            del cart[str(product_id)]
            # Save updated cart to session
            request.session['cart'] = cart
            # Return JSON response for AJAX
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart',
                'cart_count': len(cart)
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Item not found in cart'
            })
    else:
        # Fallback for non-AJAX requests
        # Get cart from session
        cart = request.session.get('cart', {})
        # Remove product from cart if it exists
        if str(product_id) in cart:
            del cart[str(product_id)]
            # Save updated cart to session
            request.session['cart'] = cart
            # Show success message
            messages.success(request, 'Item removed from cart')
        # Redirect back to sale process page with current filters
        category = request.GET.get('category', '')
        search = request.GET.get('search', '')
        return redirect(reverse('pos_app:sale_process') + f'?category={category}&search={search}' if category or search else reverse('pos_app:sale_process'))

# View for clearing the entire cart - requires user login
@login_required
def clear_cart(request):
    # Check if this is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Clear cart from session
        request.session['cart'] = {}
        # Return JSON response for AJAX
        return JsonResponse({
            'success': True,
            'message': 'Cart cleared successfully',
            'cart_count': 0
        })
    else:
        # Fallback for non-AJAX requests
        # Clear cart from session
        request.session['cart'] = {}
        # Show success message
        messages.success(request, 'Cart cleared successfully')
        # Redirect back to sale process page
        return redirect('pos_app:sale_process')

# View for sale confirmation - requires user login
@login_required
def sale_confirm(request):
    # Get cart from session
    cart = request.session.get('cart', {})
    # Check if cart is empty
    if not cart:
        messages.error(request, 'Cart is empty')
        return redirect('pos_app:sale_process')

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

    # Handle POST request for confirming sale
    if request.method == 'POST':
        # Process the sale
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
        messages.success(request, f'Sale completed successfully! Total: ₱{total_amount}')
        # Redirect to sale detail page
        return redirect('pos_app:sale_detail', pk=sale.pk)

    # Render confirmation template with cart data
    return render(request, 'pos_app/sale_confirm.html', {
        'cart_items': cart_items,
        'total': total
    })

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
    # Calculate average sale amount
    average_sale = total_sales / len(sales) if sales else 0
    # Render sales report template with data
    return render(request, 'pos_app/sales_report.html', {
        'sales': sales,
        'total_sales': total_sales,
        'average_sale': average_sale
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
