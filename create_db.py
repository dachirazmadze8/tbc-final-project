from ext import app, db
from models import Product, User

users = [{"id": 1, "username": "admin123", "password": "11111111", "role": "admin"}]

products = [
    {
        "name": "Wine",
        "price": 30,
        "img": "wine.png",
        "grape": "Saferavi",
        "region": "Qartli",
        "aroma": "White fruit",
        "taste": "Harmonious light",
        "color": "Red",
    },
    {
        "name": "Wine 2",
        "price": 10,
        "img": "wine2.png",
        "grape": "Saferavi",
        "region": "Imereti",
        "aroma": "Red fruit",
        "taste": "Velvet tannin",
        "color": "White",
    },
    {
        "name": "Wine 3",
        "price": 50,
        "img": "wine3.png",
        "grape": "Saferavi",
        "region": "Qartli",
        "aroma": "Vanilla",
        "taste": "Honey",
        "color": "Amber",
    },
]

with app.app_context():
    db.drop_all()
    db.create_all()

    for product in products:
        new_product = Product(
            name=product["name"],
            price=product["price"],
            img=product["img"],
            grape=product["grape"],
            region=product["region"],
            aroma=product["aroma"],
            taste=product["taste"],
            color=product["color"],
        )
        db.session.add(new_product)

    admin_user = User(username="admin", password="11111111", role="admin")
    db.session.add(admin_user)

    db.session.commit()
