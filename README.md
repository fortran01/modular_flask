# modular_flask

This project serves as a guide to modular architecture in back-end development, with practical examples demonstrated using the Python programming language and the Flask framework. It provides in-depth discussions of key concepts and patterns, such as the Script Pattern vs. Domain Model, various types of models in back-end systems, and the role of services in mapping requests to responses. Additionally, it covers service development techniques, dependency injection, serialization/deserialization processes, and modern development techniques like debugging, all within the context of Python and Flask. By the end of this project, participants will gain a thorough understanding of how to design and implement maintainable, scalable, and robust back-end systems using these modular architecture principles, as exemplified through Python and Flask.

## Features

<!-- TODO -->

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

The SQLite database for this project is configured and created in the `loyalty_app.py` file. The database is located in the 'instance' directory. The tables are created using SQLAlchemy's ORM and are defined in the `models.py` file. When the Flask application starts, it initializes the database and creates the tables if they do not already exist.

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
