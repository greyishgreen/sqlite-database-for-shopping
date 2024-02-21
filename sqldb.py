import sqlite3
conn=sqlite3.connect("shopping.sqlite3")
c=conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS products(
  category TEXT,
  brand TEXT,
  generalproductcode TEXT,
  productcode TEXT,
  issold BOOL

)""")
conn.commit()

c.execute("""CREATE TABLE IF NOT EXISTS customers(
  name TEXT,
  adress TEXT,
  user_id TEXT,
  card TEXT,
  phone TEXT
)""")
conn.commit()

c.execute("""CREATE TABLE IF NOT EXISTS sold_products(
  productcode TEXT,
  user_id TEXT
)""")
conn.commit()

import uuid

#user registreation system:
def sign_up():
  name=input("name:")
  adress=input("adress: ")
  user_id=str(uuid.uuid4())
  card=input("credit card info: ")
  phone=input("phone number: ")
  c.execute(f"""INSERT INTO customers VALUES(
  '{name}',
  '{adress}',
  '{user_id}',
  '{card}',
  '{phone}'
  )""")
  conn.commit()
  print("your user id is:","'" ,user_id,"'", "you can use this id to shop and view your orders")




#product registration system 
def product_register(category, brand, generalproductcode):
  
  
  issold=False 
  stock_amount=int(input("number of products in the stock: "))
  for i in range(stock_amount):
    productcode=uuid.uuid4()
    
    c.execute(f"""INSERT INTO products VALUES(
    '{category}',
    '{brand}',
    '{generalproductcode}',
    '{productcode}',
    '{issold}'
    )""")
    conn.commit()

#buying a product
def buy():
  user_id=input("your given user id:: ")
  productcode=input("product code of the product you want to buy::")

  c.execute(f"SELECT * FROM products WHERE productcode='{productcode}'")
  sonuc=c.fetchall()
  for i in sonuc:
    generalproductcode=i[2]
    if i[4]==True:
      print("the product with this code is sold out. ")
      c.execute(f"SELECT * FROM products WHERE generalproductcode='{generalproductcode}'")
      sonuc2=c.fetchall()
      print("you might want to check these products:", sonuc2 )
    else:

      c.execute(f"UPDATE products SET issold=True WHERE productcode='{productcode}'")
      conn.commit()
      c.execute(f"""INSERT INTO sold_products VALUES(
      '{productcode}',
      '{user_id}'
      )""")
  conn.commit()

  
#viewing orders
def my_orders():
  user_id=input("your given user id: ")
  c.execute(f"SELECT * FROM sold_products WHERE user_id='{user_id}'")
  sonuc=c.fetchall()
  print(sonuc)

#product filtering
def filter():
  filter=input("enter a category or a brand to search in products")
  c.execute(f"SELECT * FROM products WHERE category='{filter}' or brand='{filter}'")
  sonuc=c.fetchall()
  print(sonuc)

#viewing products
def view_products():
  c.execute("SELECT * FROM products WHERE issold=False")
  sonuc=c.fetchall()
  print(sonuc)

#returning or canceling an order
def returning():
  user_id=input("your given user id: ")
  productcode=input("product code of the product that you want to return: ")

  c.execute(f"SELECT * FROM sold_products WHERE user_id='{user_id}'")
  sonuc=c.fetchall()
  for i in sonuc:
    if i[3]==productcode:
      c.execute(f"UPDATE products SET issold=False WHERE productcode='{productcode}'")
      c.execute(f"DELETE FROM sold_products WHERE productcode='{productcode}'")
    else: 
      print("couldnt find the order. please ensure that the user id and the product code are correct")
    conn.commit()
  

