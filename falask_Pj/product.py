from flask import render_template, request, session, Blueprint, jsonify, send_from_directory

from db import *
from form import *

from datetime import datetime
import time

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
        # result = select_all_products()
        thread = myThread(target=select_all_products, args=())
        result = thread.get_result()
        products=[]
        for i in result:
            product=[]
            products.append(product)
            product.append(i[0])
            product.append(i[1])
            product.append(i[2])
            product.append(i[3])
            product.append(i[4])
            product.append(i[5])
            product.append(i[6])
            product.append(i[7])
            product.append(i[8][0:21])
            product.append(i[9])
        return render_template('products_show.html', authority=authority[1], products=products, username=username)
    else:
        return render_template('access_fail.html')

# xijiawei
# 成品管理
@product_app.route('/productInfoByCode/<productCode>', methods=['GET'])
def productInfoByCode(productCode):
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        # productType,client,uint,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk
        thread = myThread(target=select_productInfoByCode, args=(productCode,))
        productInfo = thread.get_result()
        return render_template('products_show.html', productInfo=productInfo)
    else:
        return render_template('access_fail.html')

# xijiawei
# 成品管理
@product_app.route('/productInfoByType/<productType>', methods=['GET'])
def productInfoByType(productType):
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        # productCode,client,uint,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk
        thread = myThread(target=select_productInfoByType, args=(productType,))
        productInfo = thread.get_result()
        return jsonify({'ok': True,'productInfo':productInfo})
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
                product1 = check_productInfoByCode(productCode)
                product2 = check_productInfoByType(productType)
                if not product1 and not product2:
                    print("数据库中不存在此成品。")
                    if authority[1] == '4':
                        # insert_productInfoInPart(productCode, productType, client, totalCost, materialCost, processCost, adminstrationCost, supplementaryCost, operatingCost, remark, entryTime, entryClerk)
                        myThread(target=insert_productInfoInPart, args=(productCode, productType, client, totalCost, materialCost, processCost, adminstrationCost, supplementaryCost, operatingCost, remark, entryTime, entryClerk,))
                    else:
                        # insert_productInfo(productCode, productType, client, price, profit, totalCost, taxRate, materialCost, processCost, adminstrationCost, supplementaryCost, operatingCost, remark,entryTime,entryClerk)
                        myThread(target=insert_productInfo, args=(productCode, productType, client, price, profit, totalCost, taxRate, materialCost, processCost, adminstrationCost, supplementaryCost, operatingCost, remark,entryTime,entryClerk, ))
                    for materialsOfProduct in materialsOfProductArr:
                        # insert_materialsOfProduct(productCode, materialsOfProduct[0], materialsOfProduct[1],
                        #                           materialsOfProduct[2], materialsOfProduct[3], materialsOfProduct[4],
                        #                           materialsOfProduct[5], materialsOfProduct[6])
                        myThread(target=insert_materialsOfProduct, args=(productCode, materialsOfProduct[0], materialsOfProduct[1],
                                                  materialsOfProduct[2], materialsOfProduct[3], materialsOfProduct[4],
                                                  materialsOfProduct[5], materialsOfProduct[6],))
                    for otherCosts in otherCostsArr:
                        # insert_otherCosts(productCode,otherCosts[1], otherCosts[3], otherCosts[5], otherCosts[7], otherCosts[0], otherCosts[2], otherCosts[4], otherCosts[6])
                        myThread(target=insert_otherCosts, args=(productCode,otherCosts[1], otherCosts[3], otherCosts[5], otherCosts[7], otherCosts[0], otherCosts[2], otherCosts[4], otherCosts[6],))

                    updateOfContent = "新加"
                    # insert_productChange(productCode, entryClerk, updateOfContent, entryTime)
                    myThread(target=insert_productChange, args=(productCode, entryClerk, updateOfContent, entryTime,))

                    return jsonify({'ok': "ok"})
                elif product1:
                    print("数据库中已存在同编号的成品。")
                    return jsonify({'ok': "code"})
                if product2:
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

            # productInfo = select_productInfoByCode(productCode) # productType,client,uint,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk
            thread = myThread(target=select_productInfoByCode, args=(productCode,))
            productInfo = thread.get_result()
            form.productCode.data = productCode
            form.productType.data = productInfo[0][0]
            form.client.data = productInfo[0][1]
            # productInfo[0][2] # uint
            form.price.data = productInfo[0][3]
            form.profit.data = productInfo[0][4]
            form.totalCost.data = productInfo[0][5]
            form.taxRate.data = productInfo[0][6]
            form.entryClerk.data = productInfo[0][14]
            form.remark.data = productInfo[0][12]
            form.productCode.render_kw={"class": "form-control","readonly": 'true'}
            form.productType.render_kw={"class": "form-control","readonly": 'true'}
            form.client.render_kw={"class": "form-control","readonly": 'true'}
            form.price.render_kw={"class": "form-control","readonly": 'true'}
            form.profit.render_kw={"class": "form-control","readonly": 'true'}
            form.taxRate.render_kw={"class": "form-control","readonly": 'true'}
            form.entryClerk.render_kw={"class": "form-control","readonly": 'true'}
            form.remark.render_kw={"class": "form-control","readonly": 'true'}
            materialCost = str(productInfo[0][7])
            processCost = str(productInfo[0][8])
            adminstrationCost = str(productInfo[0][9])
            supplementaryCost = str(productInfo[0][10])
            operatingCost = str(productInfo[0][11])

            # materialsOfProduct = select_materialsOfProductByCode(productCode)
            thread = myThread(target=select_materialsOfProductByCode, args=(productCode,))
            materialsOfProduct = thread.get_result()
            # otherCosts = select_otherCostsByCode(productCode)
            thread = myThread(target=select_otherCostsByCode, args=(productCode,))
            otherCosts = thread.get_result()

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
                if authority[1]=='4':
                    # update_productInfoInPart(productCode, productType, client, totalCost, materialCost, processCost, adminstrationCost, supplementaryCost, operatingCost, remark,entryTime,entryClerk)
                    myThread(target=update_productInfoInPart, args=(productCode, productType, client, totalCost, materialCost, processCost, adminstrationCost, supplementaryCost, operatingCost, remark, entryTime, entryClerk,))
                else:
                    # update_productInfo(productCode, productType, client, price, profit, totalCost, taxRate, materialCost, processCost, adminstrationCost, supplementaryCost, operatingCost, remark,entryTime,entryClerk)
                    myThread(target=update_productInfo, args=(productCode, productType, client, price, profit, totalCost, taxRate, materialCost, processCost, adminstrationCost, supplementaryCost, operatingCost, remark,entryTime,entryClerk,))
                # delete_materialsOfProduct(productCode)
                myThread(target=delete_materialsOfProduct, args=(productCode,))
                if len(materialsOfProductArr) > 0:
                    for materialsOfProduct in materialsOfProductArr:
                        # insert_materialsOfProduct(productCode, materialsOfProduct[0], materialsOfProduct[1],
                        #                           materialsOfProduct[2],
                        #                           materialsOfProduct[3], materialsOfProduct[4], materialsOfProduct[5],
                        #                           materialsOfProduct[6])
                        myThread(target=insert_materialsOfProduct,
                                 args=(productCode, materialsOfProduct[0], materialsOfProduct[1],
                                                  materialsOfProduct[2],
                                                  materialsOfProduct[3], materialsOfProduct[4], materialsOfProduct[5],
                                                  materialsOfProduct[6],))

                # delete_otherCosts(productCode)
                myThread(target=delete_otherCosts, args=(productCode,))
                for otherCosts in otherCostsArr:
                    # insert_otherCosts(productCode, otherCosts[1], otherCosts[3], otherCosts[5], otherCosts[7],
                    #                   otherCosts[0], otherCosts[2], otherCosts[4], otherCosts[6])
                    myThread(target=insert_otherCosts, args=(productCode, otherCosts[1], otherCosts[3], otherCosts[5], otherCosts[7],
                                                             otherCosts[0], otherCosts[2], otherCosts[4], otherCosts[6],))

                updateOfContent = "修改"
                # insert_productChange(productCode, entryClerk, updateOfContent, entryTime)
                myThread(target=insert_productChange, args=(productCode, entryClerk, updateOfContent, entryTime,))

                return jsonify({'ok': True})
            elif request.method == 'GET':
                # create_materialsOfProduct_temp()

                # productInfo = select_productInfoByCode(productCode)
                thread = myThread(target=select_productInfoByCode, args=(productCode,))
                productInfo = thread.get_result()
                form.productCode.data = productCode
                form.productType.data = productInfo[0][0]
                form.client.data = productInfo[0][1]
                # productInfo[0][2] # uint
                form.price.data = productInfo[0][3]
                form.profit.data = productInfo[0][4]
                form.totalCost.data = productInfo[0][5]
                form.taxRate.data = productInfo[0][6]
                form.entryClerk.data = productInfo[0][14]
                form.productCode.render_kw = {"class": "form-control", "readonly": 'true'}
                form.productType.render_kw = {"class": "form-control", "readonly": 'true'}
                form.entryClerk.render_kw = {"class": "form-control", "readonly": 'true'}
                form.remark.data = productInfo[0][12]
                materialCost = str(productInfo[0][7])
                processCost = str(productInfo[0][8])
                adminstrationCost = str(productInfo[0][9])
                supplementaryCost = str(productInfo[0][10])
                operatingCost = str(productInfo[0][11])

                # materialsOfProduct = select_materialsOfProductByCode(productCode)
                thread = myThread(target=select_materialsOfProductByCode, args=(productCode,))
                materialsOfProduct = thread.get_result()
                # otherCosts = select_otherCostsByCode(productCode)
                thread = myThread(target=select_otherCostsByCode, args=(productCode,))
                otherCosts = thread.get_result()

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
@product_app.route('/copy_product', methods=['GET', 'POST'])
def copy_product():
    if request.method == "POST":
        data = request.get_json()
        productCode = data['productCode']  # 不要写成productCode=request.data["productcode"]
        newProductCode = data['newProductCode']
        newProductType = data['newProductType']
        # copy_productInfo(productCode, newProductCode, newProductType)
        myThread(target=copy_productInfo, args=(productCode, newProductCode, newProductType,))
        # result = select_all_products()
        thread = myThread(target=select_all_products, args=())
        result = thread.get_result()
        products = []
        for i in result:
            products.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8][0:21], i[9]])
        return jsonify({'ok': True,'products':products})
    else:
        return jsonify({'ok': False})

# xijiawei
# 删除成品
@product_app.route('/delete_products', methods=['GET', 'POST'])
def delete_products():
    if session.get('username'):
        username = session['username']
        authority = select_user_authority(username)
        form = ProductForm()
        # result = select_all_products()
        thread = myThread(target=select_all_products, args=())
        result = thread.get_result()
        products = []
        for i in result:
            products.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8][0:21], i[9]])
        if request.method == "POST":
            data = request.get_json()
            productCodeArr = data['productCodeArr']  # 不要写成productCode=request.data["productcode"]
            for productCode in productCodeArr:
                # delete_productInfo(productCode)  # 注意外键约束
                myThread(target=delete_productInfo, args=(productCode,))
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
# @product_app.route('/check_uniqueness', methods=['GET', 'POST'])
# def check_uniqueness():
#     if request.method == "POST":
#         data = request.get_json()
#         materialCode = data['materialCode']  # 不要写成productCode=request.data["productcode"]
#         if check_materialInfo(materialCode):
#             material=select_materialInfoByCode(materialCode)
#             return jsonify({'ok': True,'material':material})
#         else:
#             return jsonify({'ok': False})
#     else: return jsonify({'ok': -1})

# xijiawei
# 物料编码校验
@product_app.route('/check_uniqueness', methods=['GET', 'POST'])
def check_uniqueness():
    if request.method == "POST":
        data = request.get_json()
        materialCode = data['materialCode']  # 不要写成productCode=request.data["productcode"]
        if materialCode:
            temp = check_materialInfo(materialCode)
            if temp:
                material=select_materialInfoByCode(materialCode)
                return jsonify({'ok': True,'material':material})
            else:
                return jsonify({'ok': True,'material':None})
        else:
            return jsonify({'ok': True,'material':None})
    else: return jsonify({'ok': False})

# # xijiawei
# # 查询物料
@product_app.route('/search_materials_for_options', methods=['GET', 'POST'])
def search_materials_for_options():
    if request.method == "POST":
        data = request.get_json()
        filterStr = data['filterStr']  # 不要写成productCode=request.data["productcode"]
        if filterStr:
            time.sleep(0.1)
            materials=select_materialInfoForOptions(filterStr)
            if materials:
                print(materials[0][0])
            return jsonify({'ok': True, 'materials': materials})
        else:
            return jsonify({'ok': True, 'materials': None})
    else: return jsonify({'ok': False})

# # xijiawei
# # 查询物料
@product_app.route('/search_material', methods=['GET', 'POST'])
def search_material():
    if request.method == "POST":
        data = request.get_json()
        filterStr = data['filterStr']  # 不要写成productCode=request.data["productcode"]
        if filterStr:
            print(filterStr)
            time.sleep(0.1)
            materials=select_materialInfoByFilter(filterStr)
            return jsonify({'ok': True, 'materials': materials})
        else:
            return jsonify({'ok': True, 'materials': None})
    else: return jsonify({'ok': False})

# xijiawei
# 订单管理
@product_app.route('/search_product/<filterStr>', methods=['GET'])
def search_product(filterStr):
    if session.get('username'):
        username = session['username']
        if request.method == "GET":
            thread = myThread(target=select_productInfoByFilter, args=(filterStr,))  # client, address, contact, telephone
            products = thread.get_result()
            return jsonify({'ok': True,'products':products})
    else:
        return jsonify({'ok': False})

# xijiawei
# 删除成品
@product_app.route('/product_in', methods=['GET', 'POST'])
def product_in():
    if request.method == "POST":
        data = request.get_json()
        productCode = data['productCode']  # 不要写成productCode=request.data["productcode"]
        productNum = int(data['productNum'])
        remark = data['remark']
        myThread(target=update_productInventoryNum, args=(productCode, productNum, remark,))
        return jsonify({'ok': True})
    else:
        return jsonify({'ok': False})

# # xijiawei
# # 测试
@product_app.route('/test', methods=['GET', 'POST'])
def test():
    form=UserForm()
    if request.method == "GET":
        users=select_all_users()
        sum=0
        for i in users:
            sum+=int(i[3])
        # choices=select_all_users_for_selector()
        # form.userid.choices = choices
        # return render_template('test.html',form=form,users=users,sum=sum)

        choices = select_all_users_for_selector()
        form.userid.choices = choices
        productCodeArr=["P00001","P00002","P00003"]
        products=[]
        for i in range(productCodeArr.__len__()):
            product=[]
            products.append(product)
            product.append(productCodeArr[i])
            # productInfo=select_productInfoByCode(productCodeArr[i])
            thread = myThread(target=select_productInfoByCode, args=(productCodeArr[i],))
            productInfo = thread.get_result()
            product.append(productInfo[0][0])
            product.append(i)
            # materialsOfProduct=select_materialsOfProductByCode(productCodeArr[i])
            thread = myThread(target=select_materialsOfProductByCode, args=(productCodeArr[i],))
            materialsOfProduct = thread.get_result()
            materials=[]
            product.append(materials)
            for material in materialsOfProduct:
                materials.append([material[0],material[1],material[3]])
            product.append("无")
        return render_template('test.html',form=form,users=users,sum=sum,products=products)
    elif request.method == "POST":
        re=request
        # data=request.form['personName']
        # data=form.data['personName']
        data=request.form['userid']
        data=form.data['userid']
        return data

# # xijiawei
# # 测试
@product_app.route('/test_filter', methods=['GET', 'POST'])
def test_filter():
    form=UserForm()
    if request.method == "GET":
        users=select_all_users()
        sum=0
        for i in users:
            sum+=int(i[3])
        # choices=select_all_users_for_selector()
        # form.userid.choices = choices
        # return render_template('test.html',form=form,users=users,sum=sum)

        choices = select_all_users_for_selector()
        form.userid.choices = choices
        productCodeArr=["P00001","P00002","P00003"]
        products=[]
        for i in range(productCodeArr.__len__()):
            product=[]
            products.append(product)
            product.append(productCodeArr[i])
            # productInfo=select_productInfoByCode(productCodeArr[i])
            thread = myThread(target=select_productInfoByCode, args=(productCodeArr[i],))
            productInfo = thread.get_result()
            product.append(productInfo[0][0])
            product.append(i)
            # materialsOfProduct=select_materialsOfProductByCode(productCodeArr[i])
            thread = myThread(target=select_materialsOfProductByCode, args=(productCodeArr[i],))
            materialsOfProduct = thread.get_result()
            materials=[]
            product.append(materials)
            for material in materialsOfProduct:
                materials.append([material[0],material[1],material[3]])
            product.append("无")
        return render_template('test.html',form=form,users=users,sum=sum,products=products)
    elif request.method == "POST":
        re=request
        # data=request.form['personName']
        # data=form.data['personName']
        data=request.form['userid']
        data=form.data['userid']
        return data

# # xijiawei
# # 测试
@product_app.route('/upload_download', methods=['GET', 'POST'])
def upload_download():
    if request.method == "GET":
        return send_from_directory('D:/uploads/', 'test.txt', as_attachment=True)
    elif request.method == "POST":
        file = request.files['file']
        file.save('D:/uploads/test.txt')
        return jsonify({'ok': True})
