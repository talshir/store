from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

#connect to database
connection=pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='mystore',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

@get("/admin")
def admin_portal():
    return template("pages/admin.html")

@get("/")
def index():
    return template("index.html")

@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')

@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')

@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')

#admin functions
@post('/category')
def add_category():
    cat_name = request.POST.get('name')
    if cat_name:
        cat_list = fetchCategories()
        for category in cat_list:
            if category['Name'] == cat_name:
                STATUS = "ERROR"
                MSG = "200 - Category already exists"
        insert_new_catogory(cat_name)
    else:
        STATUS = "ERROR"
        MSG = "400 - Bad Request. Please enter catoegory name"
    result = {"STATUS":STATUS, "MSG":MSG}
    return json.dumps(result)
def insert_new_category(category):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO categories(Name) VALUES ('{}')".format(category)
            cursor.execute(sql)
            connection.commit()
            STATUS = "SUCCESS"
            MSG = ""
    except Exception as e:
        STATUS = "ERROR"
        MSG = "500 - Internal Error"
    result = {"STATUS":STATUS, "MSG":MSG}
    return result

@delete('/category/<id>')
def delete_category(id):
    cat_list = fetchCategories()
    for category in cat_list:
        if category['Id'] == int(id):
            remove_category(id)
            break
    else:
        STATUS = "ERROR"
        MSG = "404 - Category not found"
        result = {"STATUS":STATUS, "MSG":MSG}
    return json.dumps(result)
def remove_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM categories WHERE Id={}".format(int(id))
            cursor.execute(sql)
            connection.commit()
            STATUS = "SUCCESS"
            MSG = ""
    except Exception as e:
        STATUS = "ERROR"
        MSG = "500 - internal error"
    result = {"STATUS":STATUS,"MSG":MSG}
    return result

@get('/categories')
def fetchCategories():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories"
            cursor.execute(sql)
            CATEGORIES = cursor.fetchall()
            STATUS = "SUCCESS"
            MSG = ""
    except Exception as e:
        STATUS = "ERROR"
        MSG = "500 - Internal Error"
    result = {"STATUS":STATUS, "CATEGORIES":CATEGORIES,"MSG":MSG}
    return json.dumps(result)

# @post('/product')
# def edit_product():
#     title = request.POST.get('title')
#     desc = request.POST.get('desc')
#     price = request.POST.get('price')
#     img_url = request.POST.get('img_url')
#     category = request.POST.get('category')
#     favorite = request.POST.get('favorite')


@get('/product/<id>')
def get_product(id):
    prod_list = fetchProducts()
    for product in prod_list:
        if product['Id'] == int(id):
            PRODUCT = product
            STATUS = "SUCCESS"
            MSG = ""
    else:
        STATUS = "ERROR"
        MSG = "404 - Product not found"
    result = {"STATUS":STATUS, "PRODUCT":PRODUCT,"MSG":MSG}
    return json.dumps(result)

@delete('/product/<id>')
def delete_product(id):
    prod_list = fetchProducts()
    for product in prod_list:
        if product['Id'] == int(id):
            remove_product(id)
            break
    else:
        STATUS = "ERROR"
        MSG = "404 - Product not found"
        result = {"STATUS":STATUS, "MSG":MSG}
    return json.dumps(result)
def remove_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM products WHERE Id={}".format(int(id))
            cursor.execute(sql)
            connection.commit()
            STATUS = "SUCCESS"
            MSG = ""
    except Exception as e:
        STATUS = "ERROR"
        MSG = "500 - internal error"
    result = {"STATUS":STATUS,"MSG":MSG}
    return result

@get('/products')
def fetchProducts():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products"
            cursor.execute(sql)
            PRODUCTS = cursor.fetchall()
            STATUS = "SUCCESS"
            MSG = ""
    except Exception as e:
        STATUS = "ERROR"
        MSG = "500 - Internal Error"
    result = {"STATUS":STATUS, "PRODUCTS":PRODUCTS,"MSG":MSG}
    return json.dumps(result)

@get('/category/<id>/products')
def fetch_products_by_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products WHERE Category_Id = {}".format(int(id))
            cursor.execute(sql)
            PRODUCTS = cursor.fetchall()
            STATUS = "SUCCESS"
            MSG = ""
    except Exception as e:
        STATUS = "ERROR"
        MSG = "500 - Internal Error"
    result = {"STATUS":STATUS, "PRODUCTS":PRODUCTS,"MSG":MSG}
    return json.dumps(result)

def main():
    run(host='localhost', port=7000)

if __name__=="__main__":
    main()