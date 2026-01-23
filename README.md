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
- Create a database named `bibliotheque`.
- Use the provided SQL files to set up the database schema and import initial data:
  - Run `src/sql/create_database.sql` to create the database tables and relationships.
  - Run `src/sql/import data.sql` to insert sample data into the tables.
- Update the `.env` file with your database credentials (e.g., host, user, password).

1. Run the application:

```sh
python src/main.py
```

## Testing

The project includes unit tests for controllers, managers, and repositories using Pytest.

To run the tests:

1. Ensure all dependencies are installed (including pytest):

```sh
pip install -r requirements.txt
```

2. Run the tests from the project root:

```sh
python -m pytest
```

Note: If `pytest` command is not available, use `python -m pytest` to run tests with the current Python environment's pytest module.

The tests are located in `src/tests/` and cover unit tests for the core components.

## Usage

- **Add Books**: Use the "Add Book" button to add new books to the library.
- **Manage Users**: Use the "Manage Users" section to add, update, or delete users.
- **Borrow and Return Books**: Track the borrowing and returning of books by users.
- **Search**: Use the search bar to find books or users based on various criteria.
