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
    data = db.get_userID(loggeduser)
    myInt = data[0][0]
    farmID = db.get_farmID(myInt)
    farms = []
    for x in farmID:
        for b in x:
            finalfarmID = b
            farms.append(b)
   
    usersfarminfo = []
    count = 0
    for x in farms:
        usersfarminfo.append(db.get_farminfo(farms[count]))
        count += 1
    farmnames = []
    count2 = 0
    for x in farms:
        farmnames.append(db.get_farmname(farms[count2]))
        count2 +=1
    productnames = []
    productnames.append(db.get_productname())

    idcount=0
    farmidint = []
    for z in farmID:
        for d in z:
            farmidint.append(farmID[idcount][0])
            idcount+=1
    
    productinfo = []
    count2 = 0
    for x in farmidint:
        productinfo.append(db.get_productinfo(farmidint[count2]))
        count2 += 1

    print(productinfo)

    finalproductinfo = []
    for x in productinfo:
        for b in x:
            finalproductinfo.append(b)

    print(finalproductinfo)

    return render_template("farm-portal.html", farminfo = usersfarminfo, names=farmnames, productnames = productnames, productinfo = finalproductinfo)

@farmportal.route("/addfarm", methods=["POST"])
def addfarm():
    db = UserDatabase(current_app.config["USERS_DB"])
    loggeduser2 = current_user.get_id()
    data2 = db.get_userID(loggeduser2)
    uid = data2[0][0]
    farmname = request.form.get("farm-name")
    description = request.form.get("open-days")
    db.insert_userfarm(farmname, description)
    newfarmid = db.get_farmidbyname(farmname)
    fid = newfarmid[0][0]
    db.insert_userandfarm(uid, fid)

    return redirect(url_for("farmportal"))

@farmportal.route("/addproduct", methods=["POST"])
def addproduct():
    db = UserDatabase(current_app.config["USERS_DB"])
    loggeduser2 = current_user.get_id()
    data2 = db.get_userID(loggeduser2)
    uid = data2[0][0]
    itemname = request.form.get("item-name")
    selectedFarm = request.form.get("farmname")
    boxes = request.form.get("boxes")
    priceperbox = request.form.get("box-price")
    pname = request.form.get("productname")
    pid = db.insert_farmProduct(pname,boxes,priceperbox,selectedFarm)
    fid = db.get_farmidbyname(selectedFarm)
    fid = fid[0][0]
    db.insert_farmProductid(fid, pid)
    db.insert_farmandproduct(pid,fid)
    myInt = data2[0][0]
    farmID = db.get_farmID(myInt)
    farmidint = []
    idcount = 0
    productid = db.get_productidbyname(pname)
    productid = productid[0][0]
    print(productid)
    db.insert_productfarm(productid, fid)
    productinfo= []
    return redirect(url_for("farmportal"))

@farmportal.route("/delete", methods=['POST'])
def delete():
    db = UserDatabase(current_app.config["USERS_DB"])
    loggeduser2 = current_user.get_id()
    data2 = db.get_userID(loggeduser2)
    uid = data2[0][0]
    farmname = request.form.get('farmnamefor')
    fid = db.get_farmidbyname(farmname)
    fid = fid[0][0]
    db.delete_farms(fid)
    db.delete_farmsellingProduct(fid)
    db.delete_productfarm(fid)
    db.delete_userfarms(fid)
    db.delete_productPerFarm(fid)

    print(farmname)
    return redirect(url_for("farmportal"))
    
   
    
