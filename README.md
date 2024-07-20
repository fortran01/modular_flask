# modular_flask

This project serves as a guide to modular architecture in back-end development, with practical examples demonstrated using the Python programming language and the Flask framework. It provides in-depth discussions of key concepts and patterns, such as the Script Pattern vs. Domain Model, various types of models in back-end systems, and the role of services in mapping requests to responses. Additionally, it covers service development techniques, dependency injection, serialization/deserialization processes, and modern development techniques like debugging, all within the context of Python and Flask. By the end of this project, participants will gain a thorough understanding of how to design and implement maintainable, scalable, and robust back-end systems using these modular architecture principles, as exemplified through Python and Flask.

## Features

- User authentication (login and logout)
- Shopping cart management (add to cart, update cart display)
- Checkout process with points calculation
- Error handling for invalid products, missing categories, and missing point earning rules
- Display of error messages for various checkout issues
- Database initialization and seeding
- Loyalty account management and point transactions

## Setup

- Clone the repository
- Create a virtual environment:

```bash
python3 -m venv venv
```

- Activate the virtual environment:

```bash
source venv/bin/activate
```

- Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start the Flask server by running:

```bash
flask --app [app_name e.g., loyalty_app] run
```

## Test Database

To create the SQLite database, you need to run the `loyalty_app.py` script directly. This is necessary because the Flask CLI does not automatically execute the code that initializes and seeds the database. By running the script directly, you ensure that the database setup code within the `app.app_context()` block is executed.

Here are the steps to run the script using the Python CLI:

1. Activate the virtual environment:

```bash
source venv/bin/activate
```

1. Run the script directly:

```bash
cd ../
ls # should see the loyalty_app.py file
python loyalty_app.py
```

To create the database and tables, the following code is used in `loyalty_app.py`:

```python
with app.app_context():
    db.create_all()
```

To seed the database with sample data, the `seed_database` function is used. This function is defined in the `seed_database.py` file and is responsible for adding sample customers, categories, products, loyalty accounts, and point earning rules to the database.

The `seed_database` function is called in the `loyalty_app.py` file when the Flask application starts, and it checks if the database is empty (e.g., no customers). If the database is empty, it seeds the database with the sample data.

Here is the relevant code snippet from `loyalty_app.py`:

```python
# Check if the database is empty (e.g., no customers)
if db.session.query(Customers).count() == 0:
    seed_database(db)
    print("Database seeded successfully")
```
