from flask import (
    Blueprint, render_template, redirect, url_for, request, flash,
    current_app
)
from flask_login import login_required
# from modules.Database.farms_db import Database
from modules.Auth.user_db import UserDatabase

farms = Blueprint(
    'farms', __name__
)

@farms.route('/')
def all_farms_view():
    db = UserDatabase(current_app.config["USERS_DB"])
    farms_data = db.select_farms()
    return render_template("farms.html", farms=farms_data)

@farms.route('/<farm_id>')
def product_view(farm_id):
    db = UserDatabase(current_app.config["USERS_DB"])
    farm_data = db.select_farm(farm_id)
    product_data = db.select_farm_product(farm_id)
    if farm_data:
        return render_template("farm.html", farm=farm_data, product=product_data)


@farms.route("/search", methods=['POST'])
def searchfield():
    db = UserDatabase(current_app.config["USERS_DB"])
    searchtext = request.form.get('searchtext')
    fid = db.get_farmidbyname(searchtext)
    fid = fid[0][0]
    farm_data=db.select_farm(fid)
    return render_template("testsearch.html", farm=farm_data)

@farms.route("/farmfilter", methods=['POST'])
def farmfilter():
    db = UserDatabase(current_app.config["USERS_DB"])
    product_array = []
    
    if request.method== 'POST':
        product_array = request.form.getlist('filter')
    productname=[]
    for x in product_array:
        print(x)
        productname.append(db.get_productidbyname(x))
    productname2= []
    count=0
    for x in productname:
        for d in x:
            productname2.append(productname[count][0])
            count += 1
    farmid=[]
    count2=0;
    for y in productname2:
        farmid.append(db.select_farmidbyproductid([count2][0])) 
        count2+=1
    print(farmid)

    finalfarmid=[] 
    for x in farmid:
        for b in x:
            finalfarmid.append(b)

    farminfo= []
    count3=0
    for x in finalfarmid:
        farminfo.append(db.get_farminfo(finalfarmid[count3][0]))
        count3+=1

    print(farminfo)
   
    return render_template("filterfarms.html", farms=farminfo)

@farms.route("/searching", methods=['POST'])
def indexsearch():
    db = UserDatabase(current_app.config["USERS_DB"])
    product_array = []
    try:
        if request.form.get("productsearch"):
            searchtext = request.form.get('searchtext')
            pid = db.get_productidbyname(searchtext)
            print(pid)
            pid = pid[0][0]
            product_data=db.select_product(pid)
            print(product_data)
            return render_template("testsearch2.html", products=product_data)
        elif request.form.get("farmsearch"):
            searchtext = request.form.get('searchtext')
            fid = db.get_farmidbyname(searchtext)
            print(fid)
            fid = fid[0][0]
            farm_data=db.select_farm(fid)
            return render_template("testsearch.html", farm=farm_data)
        flash("Incorrect search parameter")
        return render_template('index.html')
    except:
        flash("Incorrect search parameter")
        return render_template('index.html')
        