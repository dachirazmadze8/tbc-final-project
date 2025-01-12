from  flask_login import UserMixin
from ext import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product', back_populates='ratings')
    user = db.relationship('User', back_populates='ratings')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    img = db.Column(db.String)
    grape = db.Column(db.String)
    region = db.Column(db.String)
    aroma = db.Column(db.String)
    taste = db.Column(db.String)
    color = db.Column(db.String)
    ratings = db.relationship('Rating', back_populates='product', lazy='dynamic')

    @property
    def average_rating(self):
        total_ratings = sum(rating.rating for rating in self.ratings)
        count = self.ratings.count()
        return total_ratings / count if count > 0 else None


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="cart")
    items = db.relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    cart = db.relationship("Cart", back_populates="items")
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product = db.relationship("Product")
    quantity = db.Column(db.Integer, nullable=False, default=1)




class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(50), default="Guest")
    ratings = db.relationship('Rating', backref='user_ratings', lazy=True)
    cart = db.relationship("Cart", back_populates="user", uselist=False)

    def __init__(self, username, password, role="Guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)




    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()






@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



