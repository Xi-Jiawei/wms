from flask import render_template, request, session, Blueprint, jsonify

from db import *
from form import *

from datetime import datetime

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
        authority = select_user_authority(username)
        products = select_all_products()
        return render_template('products_show.html', authority=authority[1], products=products, username=username)
    else:
        return render_template('access_fail.html')

# xijiawei
# 添加成品
@product_app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form=ProductForm()
    if session.get('username'):
        username = session['username']
        authority = select_user_authority(username)
        if authority[1] == '1' or authority[1] == '2':
            return render_template('access_fail.html')
        elif authority[1]=='3' or authority[1]=='8' or authority[1]=='4':
            # if form.validate_on_submit():
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
                # entryDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                nowTime = datetime.now()
                entryTime = nowTime.strftime('%Y-%m-%d %H:%M:%S.%f')
                # entryClerk = data['entryClerk']
                entryClerk=username
                if not check_productInfoByCode(productCode) and not check_productInfoByType(productType):
                    print("数据库中不存在此成品。")
                    insert_productInfo(productCode, productType, client, price, profit, totalCost, taxRate,
                                       materialCost, processCost, adminstrationCost, supplementaryCost, operatingCost, remark,entryTime,entryClerk)
                    for materialsOfProduct in materialsOfProductArr:
                        insert_materialsOfProduct(productCode, materialsOfProduct[0], materialsOfProduct[1],
                                                  materialsOfProduct[2], materialsOfProduct[3], materialsOfProduct[4],
                                                  materialsOfProduct[5], materialsOfProduct[6])
                    for otherCosts in otherCostsArr:
                        insert_otherCosts(productCode,otherCosts[1], otherCosts[3], otherCosts[5], otherCosts[7], otherCosts[0], otherCosts[2], otherCosts[4], otherCosts[6])

                    updateOfContent = "新加"
                    insert_productChange(productCode, entryClerk, updateOfContent, entryTime)

                    return jsonify({'ok': "ok"})
                elif check_productInfoByCode(productCode):
                    print("数据库中已存在同编号的成品。")
                    return jsonify({'ok': "code"})
                elif check_productInfoByType(productType):
                    print("数据库中已存在同型号的成品。")
                    return jsonify({'ok': "type"})
            elif request.method == 'GET':
                # create_materialsOfProduct_temp()
                result=select_all_materials()
                materialCodes=[]
                for i in result:
                    materialCodes.append(i[0])
                return render_template('product_edit.html', authority=authority[1], setting=0, form=form, username=username, materialCodes=materialCodes) # setting为0表示新添，setting为1表示编辑
            else:
                # create_materialsOfProduct_temp()
                return render_template('product_edit.html', form=form, username=username)
        else:
            return render_template('access_fail.html')
    else:
        return render_template('access_fail.html')

# xijiawei
# 编辑成品
@product_app.route('/edit_product/<productCode>', methods=['GET', 'POST'])
def edit_product(productCode):
    form = ProductForm()
    if session.get('username'):
        username = session['username']
        authority = select_user_authority(username)
        if authority[1]=='2':
            print("当前权限仅限查看")

            productInfo = select_productInfoByCode(productCode) # productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk
            form.productCode.data = productCode
            form.productType.data = productInfo[0][0]
            form.client.data = productInfo[0][1]
            form.price.data = productInfo[0][2]
            form.profit.data = productInfo[0][3]
            form.totalCost.data = productInfo[0][4]
            form.taxRate.data = productInfo[0][5]
            form.entryClerk.data = productInfo[0][13]
            form.remark.data = productInfo[0][11]
            form.productCode.render_kw={"class": "form-control","readonly": 'true'}
            form.productType.render_kw={"class": "form-control","readonly": 'true'}
            form.client.render_kw={"class": "form-control","readonly": 'true'}
            form.price.render_kw={"class": "form-control","readonly": 'true'}
            form.profit.render_kw={"class": "form-control","readonly": 'true'}
            form.taxRate.render_kw={"class": "form-control","readonly": 'true'}
            form.entryClerk.render_kw={"class": "form-control","readonly": 'true'}
            form.remark.render_kw={"class": "form-control","readonly": 'true'}
            materialCost = str(productInfo[0][6])
            processCost = str(productInfo[0][7])
            adminstrationCost = str(productInfo[0][8])
            supplementaryCost = str(productInfo[0][9])
            operatingCost = str(productInfo[0][10])

            materialsOfProduct = select_materialsOfProductByCode(productCode)
            otherCosts = select_otherCostsByCode(productCode)

            return render_template('product_view.html', authority=authority[1], form=form, productCode=productCode,
                                   materialCost=materialCost,
                                   processCost=processCost, adminstrationCost=adminstrationCost,
                                   supplementaryCost=supplementaryCost, operatingCost=operatingCost,
                                   materialsOfProduct=materialsOfProduct, otherCosts=otherCosts,
                                   username=username)
        elif authority[1]=='3' or authority[1]=='8' or authority[1]=='4':
            print("当前权限可编辑")

            # if form.validate_on_submit():
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
                # entryDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                nowTime = datetime.now()
                entryTime = nowTime.strftime('%Y-%m-%d %H:%M:%S.%f')
                # entryClerk = data['entryClerk']
                entryClerk=username
                update_productInfo(productCode, productType, client, price, profit, totalCost, taxRate, materialCost,
                                   processCost, adminstrationCost, supplementaryCost, operatingCost, remark,entryTime,entryClerk)
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

                updateOfContent = "修改"
                insert_productChange(productCode, entryClerk, updateOfContent, entryTime)

                return jsonify({'ok': True})
            elif request.method == 'GET':
                # create_materialsOfProduct_temp()

                productInfo = select_productInfoByCode(productCode)
                form.productCode.data = productCode
                form.productType.data = productInfo[0][0]
                form.client.data = productInfo[0][1]
                form.price.data = productInfo[0][2]
                form.profit.data = productInfo[0][3]
                form.totalCost.data = productInfo[0][4]
                form.taxRate.data = productInfo[0][5]
                form.entryClerk.data = productInfo[0][13]
                form.productCode.render_kw = {"class": "form-control", "readonly": 'true'}
                form.productType.render_kw = {"class": "form-control", "readonly": 'true'}
                form.entryClerk.render_kw = {"class": "form-control", "readonly": 'true'}
                form.remark.data = productInfo[0][11]
                materialCost = str(productInfo[0][6])
                processCost = str(productInfo[0][7])
                adminstrationCost = str(productInfo[0][8])
                supplementaryCost = str(productInfo[0][9])
                operatingCost = str(productInfo[0][10])

                materialsOfProduct = select_materialsOfProductByCode(productCode)
                otherCosts = select_otherCostsByCode(productCode)

                result=select_all_materials()
                materialCodes=[]
                for i in result:
                    materialCodes.append(i[0])

                # setting为0表示新添，setting为1表示编辑
                return render_template('product_edit.html', authority=authority[1], setting=1, form=form, productCode=productCode, materialCost=materialCost,
                                       processCost=processCost, adminstrationCost=adminstrationCost,
                                       supplementaryCost=supplementaryCost, operatingCost=operatingCost,
                                       materialsOfProduct=materialsOfProduct, otherCosts=otherCosts, materialCodes=materialCodes,
                                       username=username)
            else:
                # create_materialsOfProduct_temp()
                return render_template('product_edit.html', form=form, username=username)
        else:
            return render_template('access_fail.html')
    else:
        return render_template('access_fail.html')

# xijiawei
# 删除成品
@product_app.route('/delete_products', methods=['GET', 'POST'])
def delete_products():
    if session.get('username'):
        username = session['username']
        authority = select_user_authority(username)
        form = ProductForm()
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
            return render_template('products_delete.html', authority=authority[1], form=form, products=products, username=username)
        else:
            return render_template('products_delete.html', authority=authority[1], form=form, products=products, username=username)
    else:
        return render_template('access_fail.html')

# xijiawei
# 物料编码校验
@product_app.route('/check_uniqueness', methods=['GET', 'POST'])
def check_uniqueness():
    if request.method == "POST":
        data = request.get_json()
        materialCode = data['materialCode']  # 不要写成productCode=request.data["productcode"]
        if check_materialInfo(materialCode):
            material=select_materialInfoByCode(materialCode)
            return jsonify({'ok': True,'material':material})
        else:
            return jsonify({'ok': False})
    else: return jsonify({'ok': -1})

# # xijiawei
# # 物料编码校验
@product_app.route('/test', methods=['GET', 'POST'])
def test():
    form=UserForm()
    if request.method == "GET":
        users=select_all_users()
        sum=0
        for i in users:
            sum+=int(i[3])
        choices=select_all_users_for_selector()
        form.userid.choices = choices
        return render_template('test.html',form=form,users=users,sum=sum)
    elif request.method == "POST":
        re=request
        # data=request.form['personName']
        # data=form.data['personName']
        data=request.form['userid']
        data=form.data['userid']
        return data
