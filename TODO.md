# TODO: Change Currency to Peso Sign (₱)

- [x] Update pos_app/templates/pos_app/sale_process.html: Replace $ with ₱ in product.price, item.subtotal, and total
- [x] Update pos_app/templates/pos_app/sale_detail.html: Replace $ with ₱ in sale.total_amount, item.unit_price, and item.total_price
- [x] Update pos_app/templates/pos_app/sales_report.html: Replace $ with ₱ in total_sales and sale.total_amount
- [x] Update pos_app/templates/pos_app/product_list.html: Replace $ with ₱ in product.price

# TODO: Enhance Sale Process with Category Selection and Search

- [x] Update pos_app/views.py: Modify sale_process view to handle category filtering and search query from GET parameters
- [x] Update pos_app/templates/pos_app/sale_process.html: Add category dropdown and search bar at the top of the products section
- [x] Test the functionality: Run server and verify category selection, product filtering, search, and cart persistence

# TODO: Add Order Summary and Confirmation

- [x] Update pos_app/views.py: Modify sale_process view to show confirmation page before completing sale
- [x] Create pos_app/templates/pos_app/sale_confirm.html: Template for order summary and confirmation
- [x] Update pos_app/templates/pos_app/sale_process.html: Change Complete Sale button to show confirmation first
- [x] Test the confirmation flow: Verify summary displays correctly and sale completes after confirmation
