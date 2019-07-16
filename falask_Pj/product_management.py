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
product_management=Blueprint('product_management',__name__)

# xijiawei
# 成品管理
@product_management.route('/product_management', methods=['GET', 'POST'])
def show_products():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        products = select_all_products()
        return render_template('show_products.html', authority=authority[1], products=products)
    else:
        return render_template('test_fail.html')

@product_management.route('/add_product', methods=['GET', 'POST'])
def add_product():
    addProductForm=AddProductForm()
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        if authority[1] == '1' or authority[1] == '2':
            return render_template('test_fail.html')
        elif authority[1]=='3':
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
                materialCost = data['materialCost']
                processCost = data['processCost']
                adminstrationCost = data['adminstrationCost']
                supplementaryCost = data['supplementaryCost']
                operatingCost = data['operatingCost']
                materialOfProductArr = data['materialOfProduct']
                otherCostsArr = data['otherCostsArr']

                if not check_productInfo(productCode):
                    print("数据库中不存在此成品。")
                    insert_productInfo(productCode, productType, client, price, profit, totalCost, taxRate,
                                       materialCost, processCost, adminstrationCost, supplementaryCost, operatingCost)
                    for materialOfProduct in materialOfProductArr:
                        insert_materialsOfProduct(productCode, materialOfProduct[0], materialOfProduct[1],
                                                  materialOfProduct[2], materialOfProduct[3], materialOfProduct[4],
                                                  materialOfProduct[5], materialOfProduct[6])
                    for otherCosts in otherCostsArr:
                        insert_otherCosts(productCode, otherCosts[0], otherCosts[1], otherCosts[2], otherCosts[3],
                                          otherCosts[4])

                    # entryDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    nowTime = datetime.now()
                    entryDate = nowTime.strftime('%Y-%m-%d %H:%M:%S.%f')
                    entryClerk = data['entryClerk']
                    updateOfContent = "新加"
                    insert_productChange(productCode, entryClerk, updateOfContent, entryDate)

                    return jsonify({'ok': True})
                else:
                    return jsonify({'ok': False})
            elif request.method == 'GET':
                create_materialsOfProduct_temp()
                return render_template('edit_product.html', setting=0, form=addProductForm)
            else:
                create_materialsOfProduct_temp()
                return render_template('edit_product.html', form=addProductForm)
        else:
            return render_template('test_fail.html')
    else:
        return render_template('test_fail.html')

@product_management.route('/edit_product/<productCode>', methods=['GET', 'POST'])
def edit_product(productCode):
    addProductForm = AddProductForm()
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        if authority[1]=='1' or authority[1]=='2':
            # do your things
            print("当前权限仅限查看")
            # return render_template('test_fail.html')

            productInfo = select_productInfoByCode(productCode)
            addProductForm.productCode.data = productCode
            addProductForm.productType.data = productInfo[0][0]
            addProductForm.client.data = productInfo[0][1]
            addProductForm.price.data = productInfo[0][2]
            addProductForm.profit.data = productInfo[0][3]
            addProductForm.totalCost.data = productInfo[0][4]
            addProductForm.taxRate.data = productInfo[0][5]
            addProductForm.productCode.render_kw={"class": "form-control","readonly": 'true'}
            addProductForm.productType.render_kw={"class": "form-control","readonly": 'true'}
            addProductForm.client.render_kw={"class": "form-control","readonly": 'true'}
            addProductForm.price.render_kw={"class": "form-control","readonly": 'true'}
            addProductForm.profit.render_kw={"class": "form-control","readonly": 'true'}
            addProductForm.taxRate.render_kw={"class": "form-control","readonly": 'true'}
            addProductForm.entryClerk.render_kw={"class": "form-control","readonly": 'true'}
            materialCost = str(productInfo[0][6])
            processCost = str(productInfo[0][7])
            adminstrationCost = str(productInfo[0][8])
            supplementaryCost = str(productInfo[0][9])
            operatingCost = str(productInfo[0][10])

            materialOfProduct = select_materialsOfProductByCode(productCode)
            otherCosts = select_otherCostsByCode(productCode)
            return render_template('view_product.html', setting=1, form=addProductForm, productCode=productCode,
                                   materialCost=materialCost,
                                   processCost=processCost, adminstrationCost=adminstrationCost,
                                   supplementaryCost=supplementaryCost, operatingCost=operatingCost,
                                   materialOfProduct=materialOfProduct, otherCosts=otherCosts)
        elif authority[1]=='3':
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
                materialCost = data['materialCost']
                processCost = data['processCost']
                adminstrationCost = data['adminstrationCost']
                supplementaryCost = data['supplementaryCost']
                operatingCost = data['operatingCost']
                materialOfProductArr = data['materialOfProduct']
                otherCostsArr = data['otherCostsArr']
                update_productInfo(productCode, productType, client, price, profit, totalCost, taxRate, materialCost,
                                   processCost, adminstrationCost, supplementaryCost, operatingCost)

                # if len(materialOfProductArr) > 0:
                #     for materialOfProduct in materialOfProductArr:
                #         if check_materialsOfProduct(productCode,materialOfProduct[0]):
                #             update_materialsOfProduct(productCode, materialOfProduct[0], materialOfProduct[1], materialOfProduct[2],materialOfProduct[3], materialOfProduct[4], materialOfProduct[5],materialOfProduct[6])
                #         else:
                #             insert_materialsOfProduct(productCode, materialOfProduct[0], materialOfProduct[1], materialOfProduct[2],materialOfProduct[3], materialOfProduct[4], materialOfProduct[5],materialOfProduct[6])
                delete_materialsOfProduct(productCode)
                if len(materialOfProductArr) > 0:
                    for materialOfProduct in materialOfProductArr:
                        insert_materialsOfProduct(productCode, materialOfProduct[0], materialOfProduct[1],
                                                  materialOfProduct[2],
                                                  materialOfProduct[3], materialOfProduct[4], materialOfProduct[5],
                                                  materialOfProduct[6])

                delete_otherCosts(productCode)
                if len(otherCostsArr) > 0:
                    for otherCosts in otherCostsArr:
                        insert_otherCosts(productCode, otherCosts[0], otherCosts[1], otherCosts[2], otherCosts[3],
                                          otherCosts[4])

                # entryDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                nowTime = datetime.now()
                entryDate = nowTime.strftime('%Y-%m-%d %H:%M:%S.%f')
                entryClerk = data['entryClerk']
                updateOfContent = "修改"
                insert_productChange(productCode, entryClerk, updateOfContent, entryDate)

                return jsonify({'ok': True})
            elif request.method == 'GET':
                create_materialsOfProduct_temp()

                productInfo = select_productInfoByCode(productCode)
                addProductForm.productCode.data = productCode
                addProductForm.productType.data = productInfo[0][0]
                addProductForm.client.data = productInfo[0][1]
                addProductForm.price.data = productInfo[0][2]
                addProductForm.profit.data = productInfo[0][3]
                addProductForm.totalCost.data = productInfo[0][4]
                addProductForm.taxRate.data = productInfo[0][5]
                materialCost = str(productInfo[0][6])
                processCost = str(productInfo[0][7])
                adminstrationCost = str(productInfo[0][8])
                supplementaryCost = str(productInfo[0][9])
                operatingCost = str(productInfo[0][10])

                materialOfProduct = select_materialsOfProductByCode(productCode)
                otherCosts = select_otherCostsByCode(productCode)
                return render_template('edit_product.html', setting=1, form=addProductForm, productCode=productCode, materialCost=materialCost,
                                       processCost=processCost, adminstrationCost=adminstrationCost,
                                       supplementaryCost=supplementaryCost, operatingCost=operatingCost,
                                       materialOfProduct=materialOfProduct, otherCosts=otherCosts)
            else:
                create_materialsOfProduct_temp()
                return render_template('edit_product.html', form=addProductForm)
        else:
            return render_template('test_fail.html')
    else:
        return render_template('test_fail.html')

# xijiawei
# jQuery测试
@product_management.route('/delete_products', methods=['GET', 'POST'])
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
            return render_template('delete_products.html', authority=authority[1], form=addProductForm, products=products)
        else:
            return render_template('delete_products.html', authority=authority[1], form=addProductForm, products=products)
    else:
        return render_template('test_fail.html')

# xijiawei
# jQuery测试
@product_management.route('/test', methods=['GET', 'POST'], defaults={"param": 15679182096})
def test(param):
    if request.method == "POST":
        # val = request.form.get('username','')
        # print(val)
        data = request.get_data()
        print("data: %s" %(data))
        json_data = request.get_json()
        print("json_data: %s" %(json_data))
        return jsonify({'ok': True})
    else: return render_template('test.html',telephone=param)

@product_management.route('/test2', methods=['GET', 'POST'])
def test2():
    if request.method == "POST":
        val = request.form
        print(val)
        return jsonify({'ok': True})
    else: return render_template('test.html')

@product_management.route('/test_table', methods=['GET', 'POST'])
def tabledata():
    if request.method == "POST":
        val = request.form
        print(val)
        return render_template('test_table.html')
    else: return render_template('test_table.html')

# xijiawei
# 创建物料组成临时表
@product_management.route('/check_uniqueness', methods=['GET', 'POST'])
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

        if check_materialOfInfo(materialCode):
            material=select_materialOfInfo(materialCode)
            return jsonify({'ok': True,'material':material})
        else:
            return jsonify({'ok': False})
    else: return jsonify({'ok': -1})