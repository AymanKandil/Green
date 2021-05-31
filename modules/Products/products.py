from flask import (
    Blueprint, render_template, redirect, url_for, request, flash,
    current_app
)
from flask_login import login_required
# from modules.Database.farms_db import Database
from modules.Auth.user_db import UserDatabase


products = Blueprint(
    'products', __name__
)

@products.route('/')
def all_products_view():
    db = UserDatabase(current_app.config["USERS_DB"])
    product_data = db.select_products()                             #Select query in database that retrieves all products
    return render_template("products.html", products=product_data)

@products.route('/<product_id>')
def product_view(product_id):
    db = UserDatabase(current_app.config["USERS_DB"])
    product_data = db.select_product(product_id)                #Takes the selected product id and retrieves product information
    farm_data = db.select_product_farm(product_id)              #Finds all farms that sell the selected product
    if product_data:
        return render_template("product-info.html", product=product_data, farms=farm_data)

@products.route('/filter', methods=['POST'])
def product_filter(): 
    db = UserDatabase(current_app.config["USERS_DB"])
    product_array = []
    if request.method== 'POST':
        product_array = request.form.getlist('filter')
    print(product_array)
    product_info = []
    for x in product_array:
        product_info.append(db.select_productsfilter(x))            #Filter that takes all selected productname and retrieves info to display

    print(product_info)
    print(product_info[0][0])
    return render_template('filterproduct.html', products=product_info)
