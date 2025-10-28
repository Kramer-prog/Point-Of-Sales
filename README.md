# Django POS (Point of Sale) System

A comprehensive Point of Sale system built with Django, designed for managing products, categories, sales transactions, and inventory in a retail environment.

## Features

- **User Authentication**: Secure login and registration for staff members.
- **Product Management**: Add, view, and manage products with categories, pricing, and stock levels.
- **Sales Processing**: Process sales transactions with cart functionality, payment methods, and automatic stock updates.
- **Inventory Tracking**: Monitor stock quantities and receive alerts for low inventory.
- **Sales Reports**: View detailed sales history and generate reports.
- **Admin Interface**: Full Django admin integration for easy data management.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8 or higher
- Pipenv (for dependency management)
- Git

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Kramer-prog/Point-Of-Sales.git
   cd Point-Of-Sales
   ```

2. **Install dependencies using Pipenv:**
   ```bash
   pipenv install
   ```

3. **Activate the virtual environment:**
   ```bash
   pipenv shell
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser account:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set up your admin username, email, and password.

## Running the Application

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the application:**
   - Open your web browser and go to `http://127.0.0.1:8000/`
   - Admin interface: `http://127.0.0.1:8000/admin/`

## Usage

### User Registration and Login

- Visit the home page and click "Register" to create a new user account.
- Log in with your credentials to access the POS system.

### Managing Products

- Navigate to the "Product List" to view all available products.
- Use the Django admin interface (`/admin/`) to add, edit, or delete products and categories.

### Processing Sales

1. Go to the "Sale Process" page.
2. Add products to your cart by clicking "Add to Cart".
3. Review your cart and select a payment method.
4. Complete the sale to update inventory and record the transaction.

### Viewing Reports

- Access the "Sales Report" page to view all sales transactions and total revenue.

## Project Structure

```
POS/
├── POS/                    # Main Django project directory
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL configuration
│   └── ...
├── pos_app/                # POS application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # App URL configuration
│   ├── admin.py            # Admin interface configuration
│   └── templates/          # HTML templates
├── db.sqlite3              # SQLite database
├── manage.py               # Django management script
├── Pipfile                 # Pipenv dependencies
└── README.md               # This file
```

## Contributing

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
=======
# Django POS (Point of Sale) System

A comprehensive Point of Sale system built with Django, designed for managing products, categories, sales transactions, and inventory in a retail environment.

## Features

- **User Authentication**: Secure login and registration for staff members.
- **Product Management**: Add, view, and manage products with categories, pricing, and stock levels.
- **Sales Processing**: Process sales transactions with cart functionality, payment methods, and automatic stock updates.
- **Inventory Tracking**: Monitor stock quantities and receive alerts for low inventory.
- **Sales Reports**: View detailed sales history and generate reports.
- **Admin Interface**: Full Django admin integration for easy data management.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8 or higher
- Pipenv (for dependency management)
- Git

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Kramer-prog/Point-Of-Sales.git
   cd Point-Of-Sales
   ```

2. **Install dependencies using Pipenv:**
   ```bash
   pipenv install
   ```

3. **Activate the virtual environment:**
   ```bash
   pipenv shell
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser account:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set up your admin username, email, and password.

## Running the Application

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the application:**
   - Open your web browser and go to `http://127.0.0.1:8000/`
   - Admin interface: `http://127.0.0.1:8000/admin/`

## Usage

### User Registration and Login

- Visit the home page and click "Register" to create a new user account.
- Log in with your credentials to access the POS system.

### Managing Products

- Navigate to the "Product List" to view all available products.
- Use the Django admin interface (`/admin/`) to add, edit, or delete products and categories.

### Processing Sales

1. Go to the "Sale Process" page.
2. Add products to your cart by clicking "Add to Cart".
3. Review your cart and select a payment method.
4. Complete the sale to update inventory and record the transaction.

### Viewing Reports

- Access the "Sales Report" page to view all sales transactions and total revenue.

## Project Structure

```
POS/
├── POS/                    # Main Django project directory
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL configuration
│   └── ...
├── pos_app/                # POS application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # App URL configuration
│   ├── admin.py            # Admin interface configuration
│   └── templates/          # HTML templates
├── db.sqlite3              # SQLite database
├── manage.py               # Django management script
├── Pipfile                 # Pipenv dependencies
└── README.md               # This file
```

## Contributing

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
=======
# Point-Of-Sales
>>>>>>> b219506d6f1ddbc3a02af2c9ee59c0cfd929ab97
