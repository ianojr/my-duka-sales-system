from flask import Flask, render_template, request, redirect, url_for,flash, session
from database import get_data,user_register,login_user, email_exist, insert_product, insert_sales, calc_profits, profits_pday, sales_pday, sales_product


app = Flask(__name__)
app.secret_key='ianojr'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/products', methods = ['POST','GET'])
def available_products():
    if "user_id" not in session:
        return redirect (url_for('login'))
    products = get_data("products")
    # print(products)
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
    if "user_id" not in session:
        return redirect(url_for("login"))
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
            # Getting the users to e in session.
            session['user_id'] = user[0]
            username = user[1]
            flash(f"welcome {username} !",)    
            return redirect(url_for("dashboard"))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect (url_for("login"))

    profits = calc_profits('sales')
    name = []
    profit = []
    for i in profits:
        name.append(str(i[0]))
        profit.append(float(i[1]))

    profits_today = profits_pday()
    day = []
    p_profit = []
    for j in profits_today:
        day.append(str(j[1]))
        p_profit.append(float(j[0]))
    
    sales_today = sales_pday()
    today = []
    sales = []
    for k in sales_today:
        today.append(str(k[1]))
        sales.append(float(k[0]))

    product_sold = sales_product()
    products = []
    sold = []
    for l in product_sold:
        products.append(str(l[1]))
        sold.append(float(l[0]))

    return render_template('dashboard.html', name = name, profit= profit, day = day, p_profit = p_profit, today = today, sales = sales, products = products, sold = sold)




if __name__ == '__main__':
    app.run(debug=True)
