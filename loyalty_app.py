from flask import Flask, request, jsonify, render_template, Response
from models import (db, Customers, LoyaltyAccounts, PointTransactions,
                    Products, Categories, PointEarningRules)
import os
from typing import List
from sqlalchemy import update
# Import the seed_database function
from seed_database import seed_database

app = Flask(__name__)
# Set a secret key for session handling
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# The SQLite database is located in the 'instance' folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loyalty_program.db'
db.init_app(app)

# Create the tables in the database if they don't exist and seed if necessary
with app.app_context():
    try:
        db.create_all()
        print("Tables created successfully")
        # Check if the database is empty (e.g., no customers)
        if db.session.query(Customers).count() == 0:
            seed_database(db)
            print("Database seeded successfully")
    except Exception as e:
        print(f"Database creation or seeding failed: {e}")


@app.route('/')
def index() -> str:
    """
    Render the index page.

    Returns:
        str: Rendered HTML of the index page.
    """
    if 'customer_id' in request.cookies:
        products: List[Products] = db.session.query(Products).all()
        return render_template('index.html', products=products, logged_in=True)
    else:
        return render_template('index.html', logged_in=False)


@app.route('/login', methods=['POST'])
def login() -> Response:
    """
    Handle customer login.

    Returns:
        Response: JSON response indicating success or failure of login.
    """
    if not request.json or 'customer_id' not in request.json:
        app.logger.error("Login attempt without customer_id")
        response = jsonify({'success': False, 'error': 'Missing customer ID'})
        response.status_code = 400
        return response

    customer_id: str = request.json['customer_id']
    app.logger.debug(f"Attempting login for customer_id: {customer_id}")

    customer: Customers | None = db.session.query(Customers).get(customer_id)
    if customer:
        response = jsonify({'success': True})
        response.set_cookie('customer_id', customer_id)
        app.logger.debug(f"Login successful for customer_id: {customer_id}")
        return response
    else:
        app.logger.error(
            f"Invalid login attempt for customer_id: {customer_id}")
        response = jsonify({'success': False, 'error': 'Invalid customer ID'})
        response.status_code = 401
        return response


@app.route('/logout')
def logout() -> Response:
    """
    Handle customer logout.

    Returns:
        Response: JSON response indicating success of logout.
    """
    response = jsonify({'success': True})
    response.delete_cookie('customer_id')
    return response


@app.route('/checkout', methods=['POST'])
def checkout() -> Response:
    """
    Handle the checkout process for the logged-in customer.

    Returns:
        Response: JSON response with total points earned and a success message
        or an error message.
    """
    if 'customer_id' in request.cookies:
        customer_id: str = request.cookies['customer_id']
        product_ids: list[int] = request.json.get(
            'product_ids', []) if request.json else []

        # Retrieve the customer's LoyaltyAccount
        loyalty_account = db.session.query(LoyaltyAccounts).filter_by(
            customer_id=customer_id).first()
        if not loyalty_account:
            response = jsonify({"error": "Loyalty account not found"})
            response.status_code = 404
            return response

        total_points_earned: int = 0
        invalid_products: List[int] = []
        products_missing_category: List[int] = []

        # For each product in the transaction
        for product_id in product_ids:
            # Determine the product's category
            product = db.session.query(Products).get(product_id)
            if not product:
                invalid_products.append(product_id)
                continue  # Skip if product is not found

            category = db.session.query(Categories).get(product.category_id)
            if not category:
                app.logger.error(
                    f"Category not found for product ID: {product_id}")
                products_missing_category.append(product_id)
                continue  # Skip if category is not found

            # Look up the applicable PointEarningRule for that category
            # Assuming the latest rule is applicable
            point_earning_rule = db.session.query(PointEarningRules) \
                .filter_by(category_id=category.id) \
                .order_by(PointEarningRules.start_date.desc()).first()

            if not point_earning_rule:
                continue  # Skip if no rule is found

            # Calculate the points earned
            product_price = float(product.price.scalar())
            points_per_dollar = point_earning_rule.points_per_dollar.scalar()
            points_earned: int = int(product_price * points_per_dollar)

            # Create a PointTransaction record
            point_transaction = PointTransactions(
                loyalty_account_id=loyalty_account.id,
                product_id=product.id,
                points_earned=points_earned,
                transaction_date=db.func.current_date()
            )
            db.session.add(point_transaction)

            total_points_earned += points_earned

        # Update the customer's LoyaltyAccount balance
        db.session.execute(
            update(LoyaltyAccounts)
            .where(LoyaltyAccounts.customer_id == customer_id)
            .values(points=LoyaltyAccounts.points + total_points_earned)
        )
        db.session.commit()

        response = jsonify({
            "total_points_earned": total_points_earned,
            "invalid_products": invalid_products,
            "products_missing_category": products_missing_category
        })
        response.status_code = 200
        return response
    else:
        response = jsonify({"error": "Customer not logged in"})
        response.status_code = 401
        return response


if __name__ == '__main__':
    print("Debug mode is:", app.debug)
    app.run(debug=True)
