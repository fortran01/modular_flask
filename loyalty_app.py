from flask import Flask, request, jsonify
from models import db, Customers, LoyaltyAccounts, PointTransactions, Products, Categories, PointEarningRules

app = Flask(__name__)

# Configure your database connection here
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loyalty_program.db'
db.init_app(app)


@app.route('/accrue_points', methods=['POST'])
def accrue_points():
    # Assume the request JSON contains the customer ID and a list of product IDs
    data = request.get_json()
    customer_id = data['customer_id']
    product_ids = data['product_ids']

    # Retrieve the customer's LoyaltyAccount
    loyalty_account = LoyaltyAccounts.query.filter_by(
        customer_id=customer_id).first()
    if not loyalty_account:
        return jsonify({"error": "Loyalty account not found"}), 404

    total_points_earned = 0

    # For each product in the transaction
    for product_id in product_ids:
        # Determine the product's category
        product = Products.query.get(product_id)
        if not product:
            continue  # Skip if product is not found

        category = Categories.query.get(product.category_id)

        # Look up the applicable PointEarningRule for that category
        point_earning_rule = PointEarningRules.query \
            .filter_by(category_id=category.id) \
            .order_by(PointEarningRules.start_date.desc()).first()  # Assuming the latest rule is applicable

        if not point_earning_rule:
            continue  # Skip if no rule is found

        # Calculate the points earned
        points_earned = product.price * point_earning_rule.points_per_dollar

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
    loyalty_account.points += total_points_earned
    db.session.commit()

    return jsonify({"total_points_earned": total_points_earned})


if __name__ == '__main__':
    app.run(debug=True)
