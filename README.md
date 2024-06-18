## Bramas Enterprises

# Car Rental Management System

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Project](#running-the-project)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction
The Car Rental Management System is a web application designed to manage car rental operations efficiently. It provides features for user registration, car listings, booking management, and location-based services.

## Features
- User Registration and Authentication
- Car Listings with Details
- Booking and Rental Management
- Location-Based Search
- Admin Dashboard for Managing Cars and Users

## Technologies Used
- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default Django database)
- **Other**: Bootstrap for UI components

## Getting Started

### Prerequisites
- Python 3.x
- Django
- Git (for version control)

### Installation
1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/car-rental-system.git
    cd car-rental-system
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run migrations:**
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser:**
    ```sh
    python manage.py createsuperuser
    ```

### Running the Project
1. **Start the development server:**
    ```sh
    python manage.py runserver
    ```

2. **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:8000/`

## Usage
- **Register** as a new user or **login** with an existing account.
- **Browse** available cars for rent.
- **Book** a car and manage your bookings.
- **Admin** can add new cars, manage users, and view booking details through the admin dashboard.
