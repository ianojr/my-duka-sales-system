import psycopg2

conn = psycopg2.connect("dbname=my_duka user=postgres password=ianojr")

cur = conn.cursor()

# cur.execute('select * from products')
# records = cur.fetchall()
# print(records)

#get products function
# def my_products ():
#     cur.execute('select * from products')
#     records = cur.fetchall()
#     return records


# # get sales sales function
# def my_sales():
#     cur.execute('select * from sales')
#     records = cur.fetchall()
#     return records

# def get_data(table):
#     data=f'select * from {table}'
#     cur.execute(data)
#     records = cur.fetchall()
#     return records

def get_data(table):
    data = f'select * from {table}'
    cur.execute(data)
    records = cur.fetchall()
    return (records)
# products = get_data('products')
# print(products)


def insert_products(values):
    data = "insert into products (name, buying_price, selling_price, stock_quantity) values (%s,%s,%s,%s)"
    cur.execute(data, values)
    conn.commit()
# data1 = ("Monitor", 2500, 5000, 54)
# inserting(data1)
# print(answer)

# User registration
def user_register(values):
    value = "insert into users (full_name, email_address, password) values (%s,%s,%s)"
    cur.execute(value, values)
    conn.commit()

# user login
def login_user( email, password):
    credentials = 'select id,full_name from users where email_address= %s and password=%s'
    cur.execute(credentials,(email, password,))
    record = cur.fetchone()
    return record

# check if email exist
def email_exist(email):
    check = 'select exists (select 1 from users where email_address = %s)'
    cur.execute(check, (email,))
    result = cur.fetchone()[0]
    return result

def insert_product(products):
    product = "insert into products (name, buying_price, selling_price, stock_quantity) values (%s,%s,%s, %s)"
    cur.execute(product, products)
    conn.commit()

def insert_sales(sales):
    sale = "insert into sales (pid, quantity, created_at) values (%s, %s, now())"
    cur.execute(sale, sales)
    conn.commit()

def calc_profits(profits):
    profit = (f"select products.name, sum((selling_price - buying_price) * quantity) as profits from {profits} inner join products on products.id = sales.pid group by products.name;")
    cur.execute(profit, profits)
    profits = cur.fetchall()
    return profits
profits = calc_profits('sales')
print(profits)

