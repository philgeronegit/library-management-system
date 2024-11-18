# Library Management System

## Overview

The Library Management System is a software application designed to manage the operations of a library. It allows users to manage books, users, and borrowing rules efficiently. The system is built using Python, PyQt6 for the graphical user interface, SQLAlchemy for database interactions, and pandas for data manipulation.

## Features

- **Book Management**: Add, update, delete, and view books in the library.
- **User Management**: Manage library users, including adding, updating, and deleting user information.
- **Borrowing Rules**: Define and manage borrowing rules such as maximum borrowing duration and late return penalties.
- **Borrowing and Returning Books**: Track the borrowing and returning of books by users.
- **Search Functionality**: Search for books and users using various criteria.
- **Data Visualization**: Display data in a tabular format with sorting and filtering capabilities.

## Technologies Used

- **Python**: The core programming language used for the application.
- **PyQt6**: Used for building the graphical user interface.
- **SQLAlchemy**: An ORM (Object-Relational Mapping) library used for database interactions.
- **pandas**: A data manipulation library used for handling data in tabular form.
- **MySQL**: The database management system used to store library data.

## Installation

1. **Clone the repository**:

```sh
git clone https://github.com/philgeronegit/library-management-system.git
cd library-management-system
```

2. Create a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required packages:

```sh
pip install -r requirements.txt
```

4. Set up the database:

- Ensure you have MySQL installed and running.
- Create a database named bibliotheque.
- Update the .env file with your database credentials.

1. Run the application:

```sh
python src/main.py
```

## Usage

- **Add Books**: Use the "Add Book" button to add new books to the library.
- **Manage Users**: Use the "Manage Users" section to add, update, or delete users.
- **Borrow and Return Books**: Track the borrowing and returning of books by users.
- **Search**: Use the search bar to find books or users based on various criteria.
