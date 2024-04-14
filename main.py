from flask import Flask, render_template, request, redirect, url_for,flash
from database import get_data,user_register,login_user, email_exist, insert_product, insert_sales, calc_profits


app = Flask(__name__)
app.secret_key='ianojr'

@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/products')
# def available_products():
#     products = get_data("products")
#     return render_template("products.html", products = products)

@app.route('/products', methods = ['POST','GET'])
def available_products():
    products = get_data("products")
    print(products)
    return render_template("products.html", products = products)


@app.route('/add_products', methods=['POST','GET'])
def inserting_products():
    if request.method == 'POST':
        name = request.form['name']
        bp = request.form['buying_price']
        sp = request.form['selling_price']
        sq = request.form['stock_quantity']
        user_inputs = (name, bp, sp, sq)
        insert_product(user_inputs)
        flash('Products Entered Successfully')
    return redirect(url_for('available_products'))

@app.route('/sales')
def sales_made():
    sales = get_data('sales')
    products = get_data('products')
    return render_template('sales.html', sales = sales, products = products)

@app.route('/add_sales', methods=["POST","GET"])
def inserting_sales():
    if request.method == 'POST':
        product_id = (request.form['pid'])
        quantity = request.form['quantity']
        add_sales = (product_id, quantity)
        insert_sales(add_sales)
        flash('Sales entered successfully')
    return redirect(url_for('sales_made'))

@app.route('/register', methods=['POST','GET'])
def register_user():
    
        if request.method == 'POST':
            f_name = request.form['full_name']
            email = request.form['email_address']
            password = request.form['password']
            user_data = (f_name, email, password)
            existing_user = email_exist(email)
            if existing_user == True:
                flash('Email already exists! Please login instead or try another email address.','danger')
                return redirect(url_for('login'))
            else:
                user_register(user_data)
                flash ('Success')
                return redirect(url_for("login"))

        return render_template('register.html')

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form["email_address"]
        password = request.form['password']
        user = login_user(email, password)
        # print(user)
        if user == None:
            flash("Please check your Email or Password!")
        else:
            username = user[1]
            flash(f"welcome {username} !",)    
            return redirect(url_for("dashboard"))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    profits = calc_profits('sales')
    name = []
    profit = []
    for i in profits:
        name.append(str(i[0]))
        profit.append(float(i[1]))
    
    return render_template('dashboard.html', name = name, profit= profit)


if __name__ == '__main__':
    app.run(debug=True)
