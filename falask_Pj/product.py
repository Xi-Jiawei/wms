import json
from datetime import timedelta
from flask import Flask, url_for, render_template, request, redirect, session, Blueprint, jsonify
from model import User
from db import *
import config
import os
from datetime import datetime

from form import *

#product_managent = Flask(__name__)
product_app=Blueprint('product',__name__)

# xijiawei
# 成品管理
@product_app.route('/products', methods=['GET', 'POST'])
def show_products():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        products = select_all_products()
        return render_template('products_show.html', authority=authority[1], products=products, username=username)
    else:
        return render_template('access_fail.html')

@product_app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    addProductForm=AddProductForm()
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        if authority[1] == '1' or authority[1] == '2':
            return render_template('access_fail.html')
        elif authority[1]=='3' or authority[1]=='8':
            # if addProductForm.validate_on_submit():
            if request.method == "POST":
                data = request.get_json()
                productCode = data['productCode']  # 不要写成productCode=request.data["productcode"]
                productType = data['productType']
                client = data['client']
                price = data['price']
                profit = data['profit']
                totalCost = data['totalCost']
                taxRate = data['taxRate']
                remark = data['remark']
                materialCost = data['materialCost']
                processCost = data['processCost']
                adminstrationCost = data['adminstrationCost']
                supplementaryCost = data['supplementaryCost']
                operatingCost = data['operatingCost']
                materialsOfProductArr = data['materialsOfProduct']
                otherCostsArr = data['otherCostsArr']
                if not check_productInfoByCode(productCode) and not check_productInfoByType(productType):
                    print("数据库中不存在此成品。")
                    insert_productInfo(productCode, productType, client, price, profit, totalCost, taxRate,
                                       materialCost, processCost, adminstrationCost, supplementaryCost, operatingCost, remark)
                    for materialsOfProduct in materialsOfProductArr:
                        insert_materialsOfProduct(productCode, materialsOfProduct[0], materialsOfProduct[1],
                                                  materialsOfProduct[2], materialsOfProduct[3], materialsOfProduct[4],
                                                  materialsOfProduct[5], materialsOfProduct[6])
                    for otherCosts in otherCostsArr:
                        insert_otherCosts(productCode,otherCosts[1], otherCosts[3], otherCosts[5], otherCosts[7], otherCosts[0], otherCosts[2], otherCosts[4], otherCosts[6])

                    # entryDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    nowTime = datetime.now()
                    entryDate = nowTime.strftime('%Y-%m-%d %H:%M:%S.%f')
                    # entryClerk = data['entryClerk']
                    entryClerk=username
                    updateOfContent = "新加"
                    insert_productChange(productCode, entryClerk, updateOfContent, entryDate)

                    return jsonify({'ok': "ok"})
                elif check_productInfoByCode(productCode):
                    print("数据库中已存在同编号的成品。")
                    return jsonify({'ok': "code"})
                elif check_productInfoByType(productType):
                    print("数据库中已存在同型号的成品。")
                    return jsonify({'ok': "type"})
            elif request.method == 'GET':
                # create_materialsOfProduct_temp()
                return render_template('product_edit.html', setting=0, form=addProductForm, username=username) # setting为0表示新添，setting为1表示编辑
            else:
                # create_materialsOfProduct_temp()
                return render_template('product_edit.html', form=addProductForm, username=username)
        else:
            return render_template('access_fail.html')
    else:
        return render_template('access_fail.html')

@product_app.route('/edit_product/<productCode>', methods=['GET', 'POST'])
def edit_product(productCode):
    addProductForm = AddProductForm()
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        if authority[1]=='1' or authority[1]=='2':
            print("当前权限仅限查看")

            productInfo = select_productInfoByCode(productCode)
            productChange = select_productChangeByCode(productCode)
            addProductForm.productCode.data = productCode
            addProductForm.productType.data = productInfo[0][0]
            addProductForm.client.data = productInfo[0][1]
            addProductForm.price.data = productInfo[0][2]
            addProductForm.profit.data = productInfo[0][3]
            addProductForm.totalCost.data = productInfo[0][4]
            addProductForm.taxRate.data = productInfo[0][5]
            addProductForm.entryClerk.data = productChange[productChange.__len__()-1][0]
            addProductForm.remark.data = productInfo[0][11]
            addProductForm.productCode.render_kw={"class": "form-control","readonly": 'true'}
            addProductForm.productType.render_kw={"class": "form-control","readonly": 'true'}
            addProductForm.client.render_kw={"class": "form-control","readonly": 'true'}
            addProductForm.price.render_kw={"class": "form-control","readonly": 'true'}
            addProductForm.profit.render_kw={"class": "form-control","readonly": 'true'}
            addProductForm.taxRate.render_kw={"class": "form-control","readonly": 'true'}
            addProductForm.entryClerk.render_kw={"class": "form-control","readonly": 'true'}
            addProductForm.remark.render_kw={"class": "form-control","readonly": 'true'}
            materialCost = str(productInfo[0][6])
            processCost = str(productInfo[0][7])
            adminstrationCost = str(productInfo[0][8])
            supplementaryCost = str(productInfo[0][9])
            operatingCost = str(productInfo[0][10])

            materialsOfProduct = select_materialsOfProductByCode(productCode)
            otherCosts = select_otherCostsByCode(productCode)

            return render_template('product_view.html', authority=authority[1], form=addProductForm, productCode=productCode,
                                   materialCost=materialCost,
                                   processCost=processCost, adminstrationCost=adminstrationCost,
                                   supplementaryCost=supplementaryCost, operatingCost=operatingCost,
                                   materialsOfProduct=materialsOfProduct, otherCosts=otherCosts,
                                   username=username)
        elif authority[1]=='3' or authority[1]=='8':
            print("当前权限可编辑")

            # if addProductForm.validate_on_submit():
            if request.method == "POST":
                data = request.get_json()
                productCode = data['productCode']  # 不要写成productCode=request.data["productcode"]
                productType = data['productType']
                client = data['client']
                price = data['price']
                profit = data['profit']
                totalCost = data['totalCost']
                taxRate = data['taxRate']
                remark = data['remark']
                materialCost = data['materialCost']
                processCost = data['processCost']
                adminstrationCost = data['adminstrationCost']
                supplementaryCost = data['supplementaryCost']
                operatingCost = data['operatingCost']
                materialsOfProductArr = data['materialsOfProduct']
                otherCostsArr = data['otherCostsArr']
                update_productInfo(productCode, productType, client, price, profit, totalCost, taxRate, materialCost,
                                   processCost, adminstrationCost, supplementaryCost, operatingCost, remark)
                delete_materialsOfProduct(productCode)
                if len(materialsOfProductArr) > 0:
                    for materialsOfProduct in materialsOfProductArr:
                        insert_materialsOfProduct(productCode, materialsOfProduct[0], materialsOfProduct[1],
                                                  materialsOfProduct[2],
                                                  materialsOfProduct[3], materialsOfProduct[4], materialsOfProduct[5],
                                                  materialsOfProduct[6])

                delete_otherCosts(productCode)
                for otherCosts in otherCostsArr:
                    insert_otherCosts(productCode, otherCosts[1], otherCosts[3], otherCosts[5], otherCosts[7],
                                      otherCosts[0], otherCosts[2], otherCosts[4], otherCosts[6])

                # entryDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                nowTime = datetime.now()
                entryDate = nowTime.strftime('%Y-%m-%d %H:%M:%S.%f')
                # entryClerk = data['entryClerk']
                entryClerk=username
                updateOfContent = "修改"
                insert_productChange(productCode, entryClerk, updateOfContent, entryDate)

                return jsonify({'ok': True})
            elif request.method == 'GET':
                # create_materialsOfProduct_temp()

                productInfo = select_productInfoByCode(productCode)
                productChange = select_productChangeByCode(productCode)
                addProductForm.productCode.data = productCode
                addProductForm.productType.data = productInfo[0][0]
                addProductForm.client.data = productInfo[0][1]
                addProductForm.price.data = productInfo[0][2]
                addProductForm.profit.data = productInfo[0][3]
                addProductForm.totalCost.data = productInfo[0][4]
                addProductForm.taxRate.data = productInfo[0][5]
                if productChange.__len__()>0:
                    addProductForm.entryClerk.data = productChange[productChange.__len__()-1][0]
                addProductForm.entryClerk.render_kw = {"class": "form-control", "readonly": 'true'}
                addProductForm.remark.data = productInfo[0][11]
                materialCost = str(productInfo[0][6])
                processCost = str(productInfo[0][7])
                adminstrationCost = str(productInfo[0][8])
                supplementaryCost = str(productInfo[0][9])
                operatingCost = str(productInfo[0][10])

                materialsOfProduct = select_materialsOfProductByCode(productCode)
                otherCosts = select_otherCostsByCode(productCode)

                # setting为0表示新添，setting为1表示编辑
                return render_template('product_edit.html', setting=1, form=addProductForm, productCode=productCode, materialCost=materialCost,
                                       processCost=processCost, adminstrationCost=adminstrationCost,
                                       supplementaryCost=supplementaryCost, operatingCost=operatingCost,
                                       materialsOfProduct=materialsOfProduct, otherCosts=otherCosts,
                                       username=username)
            else:
                # create_materialsOfProduct_temp()
                return render_template('product_edit.html', form=addProductForm, username=username)
        else:
            return render_template('access_fail.html')
    else:
        return render_template('access_fail.html')

# xijiawei
# jQuery测试
@product_app.route('/delete_products', methods=['GET', 'POST'])
def delete_products():
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        addProductForm = AddProductForm()
        products = select_all_products()
        if request.method == "POST":
            data = request.get_json()
            productCodeArr = data['productCodeArr']  # 不要写成productCode=request.data["productcode"]
            for productCode in productCodeArr:
                delete_productInfo(productCode)  # 注意外键约束
                # delete_materialsOfProduct(productCode)
                # delete_otherCosts(productCode)
            return jsonify({'ok': True})
        elif request.method == "GET":
            return render_template('products_delete.html', authority=authority[1], form=addProductForm, products=products, username=username)
        else:
            return render_template('products_delete.html', authority=authority[1], form=addProductForm, products=products, username=username)
    else:
        return render_template('access_fail.html')

# xijiawei
# 创建物料组成临时表
@product_app.route('/check_uniqueness', methods=['GET', 'POST'])
def check_uniqueness():
    if request.method == "POST":
        data = request.get_json()
        id=int(data['id'])
        materialCode = data['materialCode']  # 不要写成productCode=request.data["productcode"]

        # if check_materialsOfProduct_temp1(id):
        #     if check_materialsOfProduct_temp2(id,materialCode):
        #         print("已存在此物料。")
        #         return jsonify({'ok': True})
        #     else:
        #         update_materialsOfProduct_temp(id, materialCode)
        #         return jsonify({'ok': False})
        # else:
        #     insert_materialsOfProduct_temp(id,materialCode)
        #     return jsonify({'ok': False})

        if check_materialInfo(materialCode):
            material=select_materialInfoByCode(materialCode)
            return jsonify({'ok': True,'material':material})
        else:
            return jsonify({'ok': False})
    else: return jsonify({'ok': -1})