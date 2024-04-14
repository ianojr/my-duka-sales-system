import psycopg2

conn = psycopg2.connect("dbname=my_duka user=postgres password=ianojr")
cur = conn.cursor()


def get_data(table):
    data = f'select * from {table}'
    cur.execute(data)
    records = cur.fetchall()
    return (records)

def inserting_values(product):
    values = "insert into products (name, buying_price, selling_price, stock_quantity) values (%s,%s,%s,%s)"
    cur.execute(product,values)
    conn.commit()
    
name = input('Enter the name: ')
buying_price = input('Enter the Bp: ')
selling_price = input('Enter the Sp: ')
stock_quantity = input('Enter the quantity in stock: ')
data = (name, buying_price, selling_price, stock_quantity)
inserting_values(data)
