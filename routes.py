from flask import render_template, redirect, request,flash,url_for
from forms import ProductForm, RegisterForm, LoginForm
from os import path
from uuid import uuid4
from ext import app,db
from models import Product, User,Cart,CartItem,Rating
from flask_login import login_user,logout_user,login_required,current_user,LoginManager



@app.route('/')
def home():
    return render_template('hero.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/products')
def products():
    min_price = request.args.get("min_price", type=int)
    max_price = request.args.get("max_price", type=int)
    specific_price = request.args.get("specific_price", type=int)

    query = Product.query
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if specific_price is not None:
        query = query.filter(Product.price == specific_price)

    products = query.all()
    return render_template('index.html', products=products)



@app.route('/search')
def search():
    search_query = request.args.get('search', '').strip()

    products = Product.query.filter(Product.name.ilike(f"%{search_query}%")).all()

    return render_template('index.html', products=products)



@app.route("/createproduct", methods=["GET", "POST"])
@login_required
def create_product():
    form = ProductForm()

    if current_user.role != "admin":
        return redirect("/error")

    if form.validate_on_submit():
        try:
            file = form.img.data
            filename, filetype = path.splitext(file.filename)
            filename = f"{uuid4()}{filetype}"
            filepath = path.join(app.root_path, "static", filename)
            file.save(filepath)
        except Exception as e:
            print(f"Error saving file: {e}")
            return render_template("create_product.html", form=form, error="File upload failed")

        new_product = Product(
            name=form.name.data,
            price=float(form.price.data),
            img=filename,
            grape=form.grape.data,
            region=form.region.data,
            aroma=form.aroma.data,
            taste=form.taste.data,
            color=form.color.data
        )

        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect("/products")
        except Exception as e:
            print(f"Error saving product to database: {e}")
            db.session.rollback()
            return render_template("create_product.html", form=form, error="Failed to create product")
    else:
        print(form.errors)

    return render_template("create_product.html", form=form)


@app.route("/editproduct/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    if current_user.role != "admin":
        return redirect("/error")

    product = Product.query.get(product_id)
    if not product:
        return redirect("/error2")

    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.grape = form.grape.data
        product.region = form.region.data
        product.aroma = form.aroma.data
        product.taste = form.taste.data
        product.color = form.color.data

        if form.img.data:
            file = form.img.data
            filename, filetype = path.splitext(file.filename)
            filename = f"{uuid4()}{filetype}"
            filepath = path.join(app.root_path, "static", filename)
            file.save(filepath)
            product.img = filename

        db.session.commit()
        return redirect("/products")

    return render_template("create_product.html", form=form)


@app.route("/deleteproduct/<int:product_id>", methods=["GET", "POST"])
@login_required
def delete_product(product_id):
    if current_user.role != "admin":
        return redirect("/error")

    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect("/products")

@app.route("/product/<int:product_id>")
@login_required
def product_details(product_id):
    product = Product.query.get_or_404(product_id)

    user_rating = None
    if current_user.is_authenticated:
        existing_rating = Rating.query.filter_by(product_id=product_id, user_id=current_user.id).first()
        if existing_rating:
            user_rating = existing_rating.rating

    return render_template("product_details.html", product=product, user_rating=user_rating)



@app.route("/rate/<int:product_id>", methods=["POST"])
@login_required
def rate_product(product_id):
    rating_value = int(request.form.get("rating", 0))
    if not (1 <= rating_value <= 5):
        flash("Invalid rating. Please choose a value between 1 and 5.", "error")
        return redirect(url_for("product_details", product_id=product_id))

    existing_rating = Rating.query.filter_by(product_id=product_id, user_id=current_user.id).first()

    if existing_rating:
        existing_rating.rating = rating_value
        flash("Your rating has been updated.", "success")
    else:
        new_rating = Rating(product_id=product_id, user_id=current_user.id, rating=rating_value)
        db.session.add(new_rating)
        flash("Thank you for your rating!", "success")

    db.session.commit()
    return redirect(url_for("product_details", product_id=product_id))





@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    if current_user.cart is None:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    else:
        cart = current_user.cart
    cart_item = CartItem.query.filter_by(product_id=product.id, cart_id=cart.id).first()
    quantity = int(request.form.get("quantity", 1))  # Default to 1 if not provided

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    flash(f"{product.name} added to your cart!", "success")
    return redirect(url_for("product_details", product_id=product.id))


@app.route('/cart')
@login_required
def view_cart():
    if not current_user.cart:
        flash("You don't have any items in your cart yet.", "info")
        return redirect(url_for('home'))

    cart_items = current_user.cart.items
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route("/remove_from_cart/<int:cart_item_id>", methods=["POST"])
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)

    if cart_item.cart.user_id != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("view_cart"))

    db.session.delete(cart_item)
    db.session.commit()
    flash("Item removed from cart.", "success")
    return redirect(url_for("view_cart"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect("/register")

        if len(form.password.data) < 8 or len(form.password.data) > 32:
            flash("Password must be between 8 and 32 characters.", "error")
            return redirect("/register")

        if form.password.data != form.repeat_password.data:
            flash("Passwords do not match. Please try again.", "error")
            return redirect("/register")

        new_user = User(username=form.username.data, password=form.password.data, role="Guest")
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! You can now log in.", "success")
        return redirect("/login")

    return render_template("register_account.html", form=form)



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        else:
            flash("Invalid username or password","error")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/error")
def error():
    return render_template('error.html')

@app.route("/error2")
def error2():
    return render_template('error2.html')

@app.before_request
def ensure_user_has_cart():
    if current_user.is_authenticated and not current_user.cart:
        new_cart = Cart(user_id=current_user.id)
        db.session.add(new_cart)
        db.session.commit()


