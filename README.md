# BookMart

"Book Mart" is destination for digital literature, offering a seamless online platform where readers can discover, purchase, and enjoy their favorite books with ease. With a curated selection of e-books and a library of free audiobooks, "Book Mart" caters to the diverse tastes and preferences of readers worldwide. Our user-friendly interface allows customers to browse, purchase, and download books in PDF format effortlessly.

# Installation

Before installing the project, make sure you have the following installed:
- Python (3.11.3 recommended)
- pip (Python package installer)

# Setting up the environment

It's recommended to use a virtual environment to manage the dependencies and keep them separate from other projects. Here’s how you can set up a virtual environment:

# Install virtualenv if it's not installed
pip install virtualenv

# Create a virtual environment

virtualenv venv

# Activate the virtual environment

# On Windows

venv\Scripts\activate

# On MacOS/Linux

source venv/bin/activate

# Installing dependencies

Once your environment is ready, you can install the required Python packages using pip:

# Navigate to the project directory

cd path/to/bookmart

# Install Django and other dependencies from the requirements file

pip install -r requirements.txt

# Setting up the database

This project uses SQLite, which is Django's default database. You will need to set up the initial database and run migrations as follows:

# Run migrations to create the database schema

python manage.py makemigrations
python manage.py migrate

# Running the server

Now you're ready to run the development server and see the project in action:

# Run the Django development server

python manage.py runserver

# Accessing the Application

Once the server is running, you can access different parts of the application using the following URLs:

# Home Page

Navigate to http://127.0.0.1:8000/ in your web browser to view the main page of the application.

# Admin Interface

Navigate to http://127.0.0.1:8000/myadminapp to access the admin interface.

Login with the following credentials:
Email: admin@gmail.com
Password: 123

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('myapp.urls')),
    path("mydminapp", include('mydminapp.urls')),
    path("supplier", include('supplier.urls')),
]

# urls.py for admin interface
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("myapp", include('myapp.urls')),
    path("", include('mydminapp.urls')),
    path("supplier", include('supplier.urls')),
]
# Supplier Page

Navigate to http://127.0.0.1:8000/supplier to view the supplier page.

Login with the following credentials:
Email: priti@gmail.com
Password: priti

# urls.py for supplier page
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("myapp", include('myapp.urls')),
    path("mydminapp", include('mydminapp.urls')),
    path("", include('supplier.urls')),
]
