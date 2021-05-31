from flask import (
    Blueprint, render_template, redirect, url_for, request, flash,
    current_app
)
from flask_login import login_required, current_user
from modules.Auth.user_db import UserDatabase
from models import requires_access_level
import numpy as np
from itertools import chain, product



farmportal = Blueprint(
    'farmportal', __name__
)

@farmportal.route("/")
@login_required
def farmer_view():
    db = UserDatabase(current_app.config["USERS_DB"])               
    loggeduser = current_user.get_id()
    data = db.get_userID(loggeduser)                                    #Gets user id
    myInt = data[0][0]
    farmID = db.get_farmID(myInt)                                       #Gets all farm ids linked to user
    farms = []
    for x in farmID:
        for b in x:
            finalfarmID = b
            farms.append(b)                                          #Puts the farm id into array of integars
   
    usersfarminfo = []
    count = 0
    for x in farms:
        usersfarminfo.append(db.get_farminfo(farms[count]))                     #Gets the farm info in the farm id's in the array
        count += 1
    farmnames = []
    count2 = 0
    for x in farms:
        farmnames.append(db.get_farmname(farms[count2]))                        #Gets all the farm names from the array
        count2 +=1
    productnames = []
    productnames.append(db.get_productname())

    idcount=0
    farmidint = []
    for z in farmID:
        for d in z:
            farmidint.append(farmID[idcount][0])                               #Gets the id into an array of integars instead of a tuple
            idcount+=1
    
    productinfo = []
    count2 = 0
    for x in farmidint:
        productinfo.append(db.get_productinfo(farmidint[count2]))              #Gets the product info based on which farm id is linked to the product id
        count2 += 1 

    print(productinfo)

    finalproductinfo = []
    for x in productinfo:
        for b in x:
            finalproductinfo.append(b)                      #Appends the retrieved information into an array instead of a tuple

    print(finalproductinfo)

    return render_template("farm-portal.html", farminfo = usersfarminfo, names=farmnames, productnames = productnames, productinfo = finalproductinfo)

@farmportal.route("/addfarm", methods=["POST"])
def addfarm():
    db = UserDatabase(current_app.config["USERS_DB"])
    loggeduser2 = current_user.get_id()
    data2 = db.get_userID(loggeduser2)
    uid = data2[0][0]
    farmname = request.form.get("farm-name")                    #Takes the farm name from the form
    description = request.form.get("open-days")                 #takes the description from the form
    db.insert_userfarm(farmname, description)                   #Database query to insert it into database
    newfarmid = db.get_farmidbyname(farmname)                   #Takes the id of the recently inserted farm
    fid = newfarmid[0][0]   
    db.insert_userandfarm(uid, fid)                             #Creates a copy of the userid and the farm id of new farm in relation database

    return redirect(url_for("farmportal"))

@farmportal.route("/addproduct", methods=["POST"])
def addproduct():
    db = UserDatabase(current_app.config["USERS_DB"])
    loggeduser2 = current_user.get_id()
    data2 = db.get_userID(loggeduser2)
    uid = data2[0][0]
    itemname = request.form.get("item-name")
    selectedFarm = request.form.get("farmname")                 #Takes the farm selected from dropdown
    boxes = request.form.get("boxes")                           #Takes amount of boxes
    priceperbox = request.form.get("box-price")                 #Takes price of boxes
    pname = request.form.get("productname")                     #Takes selected product
    pid = db.insert_farmProduct(pname,boxes,priceperbox,selectedFarm)       #Inserts the farm and product query into database
    fid = db.get_farmidbyname(selectedFarm)                                 #Gets farm id of the selected farm
    fid = fid[0][0]
    db.insert_farmProductid(fid, pid)                               #Inserts product and farm id into relations table in databse for which farm has product
    db.insert_farmandproduct(pid,fid)                               #Inserts product and farm id into relations table in database for which farm is selling specfic product
    myInt = data2[0][0]
    farmID = db.get_farmID(myInt)
    farmidint = []
    idcount = 0
    productid = db.get_productidbyname(pname)                      #Gets product id of the prodcuct that was selected
    productid = productid[0][0]
    db.insert_productfarm(productid, fid)                          #Insert product and farm into a relation table
    productinfo= []
    return redirect(url_for("farmportal"))

@farmportal.route("/delete", methods=['POST'])
def delete():
    db = UserDatabase(current_app.config["USERS_DB"])
    loggeduser2 = current_user.get_id()
    data2 = db.get_userID(loggeduser2)
    uid = data2[0][0]
    farmname = request.form.get('farmnamefor')                  #Takes selected farm from drop down in the form
    fid = db.get_farmidbyname(farmname)                         #SELECT query for the farm id from the selected farm name
    fid = fid[0][0]
    db.delete_farms(fid)                                        #   Deletes from farm table query
    db.delete_farmsellingProduct(fid)                           #   Deletes from FarmSellingProduct table
    db.delete_productfarm(fid)                                  #   Deletes from productFarm table
    db.delete_userfarms(fid)                                    #   Deletes from userFarms table
    db.delete_productPerFarm(fid)                               #   Deletes from productPerFarm table

    return redirect(url_for("farmportal"))
    
@farmportal.route("/update", methods=['POST'])
def update():
    db = UserDatabase(current_app.config["USERS_DB"])
    loggeduser2 = current_user.get_id()
    data2 = db.get_userID(loggeduser2)
    uid = data2[0][0]
    farmname = request.form.get('farmname')
    fid = db.get_farmidbyname(farmname)
    fid = fid[0][0]
    newname = request.form.get('nfarm-name')                #Retrieves new name from form
    newdesc = request.form.get('ndesc')                     #Retrieves description from form
    db.update_farm(newname, newdesc, fid)                   #Updates query for database to change name and description of farm
    db.update_productperfarm(newname,fid)                   #Updates the productPerFarm table with new farm table

    print(farmname)
    return redirect(url_for("farmportal"))
    
    
