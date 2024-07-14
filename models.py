from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey


class Base(DeclarativeBase):
    """
    Base class for all models.
    DeclarativeBase is a base class provided by SQLAlchemy's ORM.
    It is used to define the base class for all ORM-mapped classes.
    By inheriting from DeclarativeBase, the models can be defined using a
    declarative style, where the table structure and class definitions are
    combined in a single class definition.
    This approach allows for a more Pythonic and intuitive way to define
    database models.
    """
    pass


db: SQLAlchemy = SQLAlchemy(model_class=Base)


class Customers(Base):
    """
    Represents a customer in the database.

    Attributes:
        id (int): Unique identifier for the customer.
        name (str): Name of the customer.
        email (str): Email address of the customer.
    """
    __tablename__: str = 'Customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))


class LoyaltyAccounts(Base):
    """
    Represents a loyalty account in the database.

    Attributes:
        id (int): Unique identifier for the loyalty account.
        customer_id (int): Identifier for the associated customer.
        points (int): Current points balance of the loyalty account.
        customer (relationship): Relationship to the associated customer.
    """
    __tablename__: str = 'LoyaltyAccounts'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('Customers.id'))
    points = Column(Integer, default=0)
    customer = relationship('Customers', backref='loyalty_accounts', lazy=True)


class PointTransactions(Base):
    """
    Represents a point transaction in the database.

    Attributes:
        id (int): Unique identifier for the point transaction.
        loyalty_account_id (int): Identifier for the associated loyalty
                                  account.
        product_id (int): Identifier for the associated product.
        points_earned (int): Number of points earned in the transaction.
        transaction_date (date): Date when the transaction occurred.
        loyalty_account (relationship): Relationship to the associated loyalty
                                        account.
        product (relationship): Relationship to the associated product.
    """
    __tablename__: str = 'PointTransactions'
    id = Column(Integer, primary_key=True)
    loyalty_account_id = Column(Integer, ForeignKey('LoyaltyAccounts.id'))
    product_id = Column(Integer, ForeignKey('Products.id'))
    points_earned = Column(Integer)
    transaction_date = Column(Date)
    loyalty_account = relationship(
        'LoyaltyAccounts', backref='point_transactions', lazy=True)
    product = relationship('Products', backref='point_transactions', lazy=True)


class Products(Base):
    """
    Represents a product in the database.

    Attributes:
        id (int): Unique identifier for the product.
        name (str): Name of the product.
        price (Numeric): Price of the product.
        category_id (int): Identifier for the associated category.
        image_url (str): URL of the product image.
        category (relationship): Relationship to the associated category.
    """
    __tablename__: str = 'Products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(Numeric(10, 2))
    category_id = Column(Integer, ForeignKey('Categories.id'))
    image_url = Column(String(255))  # Add the image_url field
    category = relationship('Categories', backref='products', lazy=True)


class Categories(Base):
    """
    Represents a category in the database.

    Attributes:
        id (int): Unique identifier for the category.
        name (str): Name of the category.
    """
    __tablename__: str = 'Categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class PointEarningRules(Base):
    """
    Represents a point earning rule in the database.

    Attributes:
        id (int): Unique identifier for the point earning rule.
        category_id (int): Identifier for the associated category.
        points_per_dollar (int): Ratio of points earned per dollar spent.
        start_date (date): Start date for when the rule is applicable.
        end_date (date): End date for when the rule is no longer applicable.
        category (relationship): Relationship to the associated category.
    """
    __tablename__: str = 'PointEarningRules'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('Categories.id'))
    points_per_dollar = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    category = relationship(
        'Categories', backref='point_earning_rules', lazy=True)
