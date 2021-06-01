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
    db = UserDatabase(current_app.config["USERS_DB"])               #Connects to database
    farms_data = db.select_farms()                                  #Uses select_farms database query to select all farms
    return render_template("farms.html", farms=farms_data)          #Renders all the current farms stored in database

@farms.route('/<farm_id>')
def product_view(farm_id):
    db = UserDatabase(current_app.config["USERS_DB"])           
    farm_data = db.select_farm(farm_id)                 #Selects farm based on farmID
    product_data = db.select_farm_product(farm_id)      #Select products linked to selected farm above
    if farm_data:
        return render_template("farm-info.html", farm=farm_data, product=product_data)      #Shows the specfic farm's page by using the Farm ID for the url and checking which farm
                                                                                            #Was selected


@farms.route("/search", methods=['POST'])
def searchfield():
    db = UserDatabase(current_app.config["USERS_DB"])
    searchtext = request.form.get('searchtext')             #Takes the inputed text in search bar
    fid = db.get_farmidbyname(searchtext)                   #Finds the farmID by the name inputed in search bar
    fid = fid[0][0]                                         #Extracts the farm id from the tuple into and integar
    farm_data=db.select_farm(fid)                           #Selects farm based on id
    return render_template("testsearch.html", farm=farm_data)       #Displays selected farm

@farms.route("/farmfilter", methods=['POST'])
def farmfilter():
    db = UserDatabase(current_app.config["USERS_DB"])
    product_array = []
    
    if request.method== 'POST':
        product_array = request.form.getlist('filter')          #Gets the selected checkboxes in filters
    productname=[]  
    for x in product_array:                                     #Using the selected checkboxes a for loop goes through each and gets their id
        
        productname.append(db.get_productidbyname(x))
    productname2= []
    count=0
    for x in productname:
        for d in x:
            productname2.append(productname[count][0])              #Nested for loop to get  the id as an array of integars
            count += 1
    farmid=[]
    count2=0;
    for y in productname2:
        farmid.append(db.select_farmidbyproductid(productname2[count2][0]))                     #For loop to get the farm id from the product id using the database query
        count2+=1
    

    finalfarmid=[] 
    for x in farmid:
        for b in x:
            finalfarmid.append(b)

    farminfo= []
    count3=0
    for x in finalfarmid:
        farminfo.append(db.get_farminfo(finalfarmid[count3][0]))                    #Gets the farm data from the farm ids we set in the previous for loops.
        count3+=1
    return render_template("filterfarms.html", farms=farminfo)

@farms.route("/searching", methods=['POST'])
def indexsearch():
    db = UserDatabase(current_app.config["USERS_DB"])
    product_array = []
    try:
        if request.form.get("productsearch"):                                           #Checks which checkbox is selected to narrow search
            searchtext = request.form.get('searchtext')                         
            pid = db.get_productidbyname(searchtext)                                    #Finds the productid based on name inputted in checkbox
            pid = pid[0][0]
            product_data=db.select_product(pid)                                         #Selects product based on product id
            return render_template("testsearch2.html", products=product_data)
        elif request.form.get("farmsearch"):                                            #Checks if its the farm checkbox that is selected
            searchtext = request.form.get('searchtext')                                 #Takes the text in search box and stores it
            fid = db.get_farmidbyname(searchtext)                                       #Finds farm id based on name
            fid = fid[0][0]
            farm_data=db.select_farm(fid)                                               #Retrieves farm data to display
            return render_template("testsearch.html", farm=farm_data)
        flash("Incorrect search parameter")
        return render_template('index.html')
    except:
        flash("Incorrect search parameter")
        return render_template('index.html')
        