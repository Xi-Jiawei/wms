from flask import render_template, request, session, Blueprint, jsonify
from datetime import datetime

from db import *
from form import *

procurement_app=Blueprint('procurement',__name__)

# xijiawei
# 采购记录
@procurement_app.route('/procurement_history', methods=['GET'])
def procurement_history():
    addProductForm = AddProductForm()
    print(session)
    print(session.keys())
    print(session.get('username'))
    if request.method == 'GET':
        if session.get('username'):
            username = session['username']
            authority = login_Authority(username)
            all_procurements = select_procurement() # count(p.procurementCode),procurementCode,productCode,materialCodeConcatStr,materialNameConcatStr,materialNumConcatStr,productType,productNum,client,entryClerk,entryDate
            procurements=[]
            procurementCode=''
            for i in all_procurements:
                if not i[1]==procurementCode:
                    procurementCode = i[1]
                    procurement=[]
                    product=[]
                    procurements.append(procurement)
                    procurement.append(i[0]) # count(p.procurementCode)
                    procurement.append(i[1]) # procurementCode
                    product.append([i[2],i[6],i[7],i[3],i[4],i[5]]) # productCode,productType,productNum,materialCodeConcatStr,materialNameConcatStr,materialNumConcatStr
                    procurement.append(product)
                    procurement.append(i[8]) # client
                    procurement.append(i[9]) # entryClerk
                    procurement.append(i[10]) # entryDate
                else:
                    product.append([i[2], i[6], i[7],i[3],i[4],i[5]])
            return render_template('procurement_history.html', form=addProductForm,
                                   procurements=procurements,
                                   authority=authority[2],
                                   username=username)
        else:
            return render_template('access_fail.html')

# xijiawei
# 删除采购，撤消某次采购
@procurement_app.route('/delete_procurements', methods=['POST'])
def delete_procurements():
    if request.method == "POST":
        data = request.get_json()
        procurementCodeArr = data['procurementCodeArr']
        for procurementCode in procurementCodeArr:
            delete_procurementByCode(procurementCode)
        return jsonify({'ok': True})
    else:
        return jsonify({'ok': False})

# xijiawei
# 实时计算生成采购清单
@procurement_app.route('/calculate_procurement', methods=['GET', 'POST'])
def calculate_procurement():
    if request.method == "POST":
        data = request.get_json()
        productCodeOrTypeInputArr = data['productCodeOrTypeInputArr']
        productCodeOrType = data['productCodeOrType']
        productNumArr = data['productNumArr']
        url=data['url']

        # productCode and productType
        productCodeArr = []
        productTypeArr = []
        if productCodeOrType == "0":
            productCodeArr = productCodeOrTypeInputArr
            for productCode in productCodeArr[0:len(productCodeArr) - 1]:
                if select_productTypeByCode(productCode):
                    productTypeArr.append(select_productTypeByCode(productCode)[0][0])
                else:
                    return jsonify({'ok': False})
            if select_productTypeByCode(productCodeArr[len(productCodeArr) - 1]):
                productTypeArr.append(select_productTypeByCode(productCodeArr[len(productCodeArr) - 1])[0][0])
            else:
                productCodeArr.pop(len(productCodeArr) - 1)
        elif productCodeOrType == "1":
            productTypeArr = productCodeOrTypeInputArr
            # productTypeArrTemp=productTypeArr[0:len(productTypeArr) - 1]
            for productType in productTypeArr[0:len(productTypeArr) - 1]:
                if select_productCodeByType(productType):
                    productCodeArr.append(select_productCodeByType(productType)[0][0])
                else:
                    return jsonify({'ok': False})
            if select_productCodeByType(productTypeArr[len(productTypeArr) - 1]):
                productCodeArr.append(select_productCodeByType(productTypeArr[len(productTypeArr) - 1])[0][0])
            else:
                productTypeArr.pop(len(productTypeArr) - 1)

        # productNum
        if len(productNumArr)<len(productCodeArr):
            for i in range(len(productCodeArr)-len(productNumArr)):
                productNumArr.append(0)

        # materials
        products = []
        for i in range(productCodeArr.__len__()):
            materialsOfProduct = select_materialsOfProductByCode(productCodeArr[i])  # materialCode,,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost
            productInfo = select_productInfoByCode(productCodeArr[i])  # productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk
            product = []
            material = []
            product.append(productCodeArr[i])
            product.append(productInfo[0][0])
            product.append(productNumArr[i])
            for materialOfProduct in materialsOfProduct:
                materialInfo = select_materialInfoByCode(materialOfProduct[0])  # materialName,materialType,remark,inventoryNum,price,inventoryMoney,supplier
                material.append([materialOfProduct[0], materialInfo[0][0], materialOfProduct[1]])
            product.append(material)
            # productCode,productType,productNum,[materialCode,materialName,materialNum]
            products.append(product)
            update_productNumOfProductInfo(productCodeArr[i], productNumArr[i]) # 更新productNum字段，以便采购时进行物料汇总计算
        materials=select_materialsOfProductByCodeArr(productCodeArr) # materialCode,materialName,unit,inventoryNum,materialNum,(inventoryNum-materialNum),supplier
        result={'products':products,'materials':materials}
        return jsonify({'ok': True, 'result': result})
    else: return jsonify({'ok': -1})

# xijiawei
#
@procurement_app.route('/productTypeByCode', methods=['GET', 'POST'])
def productTypeByCode():
    if request.method == "POST":
        data = request.get_json()
        productCodeArr = data['productCodeArr']  # 不要写成productCode=request.data["productcode"]
        productTypeArr = [0 for key in range(len(productCodeArr))]
        for i in range(len(productCodeArr)):
            productTypeArr[i]=select_productTypeByCode(productCodeArr[i])
        return jsonify({'ok': True, 'productTypeArr': productTypeArr})
    else: return jsonify({'ok': -1})

# xijiawei
#
@procurement_app.route('/productCodeByType', methods=['GET', 'POST'])
def productCodeByType():
    if request.method == "POST":
        data = request.get_json()
        productTypeArr = data['productTypeArr']  # 不要写成productCode=request.data["productcode"]
        productCodeArr = [0 for key in range(len(productTypeArr))]
        for i in range(len(productTypeArr)):
            productCodeArr[i]=select_productCodeByType(productTypeArr[i])
        return jsonify({'ok': True, 'productCodeArr': productCodeArr})
    else: return jsonify({'ok': -1})

# xijiawei
# 添加采购
@procurement_app.route('/procurement', methods=['GET', 'POST'])
def procurement():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        if request.method == "POST":
            data = request.get_json()
            productCodeOrTypeInputArr = data['productCodeOrTypeInputArr']
            productCodeOrType = data['productCodeOrType']
            productNumArr = data['productNumArr']
            client = data['client']
            if session.get('username'):
                entryClerk = session['username']
            else:
                entryClerk = "unknown"
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            # productCode and productType
            productCodeArr=[]
            productTypeArr=[]
            if productCodeOrType == "0":
                productCodeArr = productCodeOrTypeInputArr
                if not select_productTypeByCode(productCodeArr[len(productCodeArr) - 1]):
                    return jsonify({'ok': False})
                else:
                    for productCode in productCodeArr:
                        productTypeArr.append(select_productTypeByCode(productCode)[0][0])
            elif productCodeOrType == "1":
                productTypeArr = productCodeOrTypeInputArr
                if not select_productCodeByType(productTypeArr[len(productTypeArr) - 1]):
                    return jsonify({'ok': False})
                else:
                    for productType in productTypeArr:
                        productCodeArr.append(select_productCodeByType(productType)[0][0])

            # procurementCode=uuid.uuid1() # 使用uuid生成唯一代号
            procurementCode=datetime.now().strftime('%Y%m%d%H%M%S%f') # 使用时间戳生成唯一代号
            procurementCode=procurementCode[0:16] # 使用时间戳生成唯一代号
            for i in range(productCodeArr.__len__()):
                insert_procurement(procurementCode, productCodeArr[i], int(productNumArr[i]), client, "null", entryClerk, entryTime)
            return jsonify({'ok': True})
        elif request.method == 'GET':
            addProductForm = AddProductForm()
            return render_template('procurement.html', setting=0, form=addProductForm, authority=authority[2],username=username)
    else:
        return render_template('access_fail.html')

# xijiawei
# 修改采购
@procurement_app.route('/edit_procurement/<procurementCode>', methods=['GET', 'POST'])
def edit_procurement(procurementCode):
    print(session)
    print(session.keys())
    print(session.get('username'))
    addProductForm = AddProductForm()
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)

        # POST
        if request.method == "POST":
            data = request.get_json()
            productCodeOrTypeInputArr = data['productCodeOrTypeInputArr']
            productCodeOrType = data['productCodeOrType']
            productNumArr = data['productNumArr']
            client = data['client']
            if session.get('username'):
                entryClerk = session['username']
            else:
                entryClerk = "unknown"
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            # productCode and productType
            productCodeArr=[0 for key in range(len(productCodeOrTypeInputArr))]
            productTypeArr=[0 for key in range(len(productCodeOrTypeInputArr))]
            if productCodeOrType == "0":
                productCodeArr = productCodeOrTypeInputArr
                if not select_productTypeByCode(productCodeArr[len(productCodeArr) - 1]):
                    return jsonify({'ok': False})
                else:
                    for i in range(len(productCodeArr)):
                        productType = select_productTypeByCode(productCodeArr[i])
                        productTypeArr[i]=productType[0][0]
            elif productCodeOrType == "1":
                productTypeArr = productCodeOrTypeInputArr
                if not select_productCodeByType(productTypeArr[len(productTypeArr) - 1]):
                    return jsonify({'ok': False})
                else:
                    for i in range(len(productTypeArr)):
                        productCode = select_productCodeByType(productTypeArr[i])
                        productCodeArr[i] = productCode[0][0]

            # update procurement and update materialInfo
            delete_procurementByCode(procurementCode) # 撤回上次采购
            for i in range(productCodeArr.__len__()):
                insert_procurement(procurementCode, productCodeArr[i], int(productNumArr[i]), client, "null", entryClerk, entryTime)
            return jsonify({'ok': True})
        elif request.method == 'GET':
            all_products = select_procurementByCode(procurementCode) # productCode,productType,productNum,client,remark,materialCode,materialName,materialNum
            products = []
            productCode = ''
            productCodeInput = ''
            productTypeInput = ''
            productNumInput = ''
            for i in all_products:
                if not i[0] == productCode:
                    productCode = i[0]
                    product = []
                    material = []
                    product.append(i[0])  # productCode
                    if i[1]:
                        product.append(i[1])  # productType
                    else:
                        product.append("")
                    product.append(i[2])  # productNum
                    if i[5] and i[6] and i[7]:
                        material.append([i[5], i[6], i[7]])  # materialCode,materialName,materialNum
                    else:
                        material.append(["","",""])
                    product.append(material)
                    product.append(i[4])  # remark
                    # productCode,productType,productNum,[materialCode,materialName,materialNum],remark
                    products.append(product)

                    # form data
                    productCodeInput+=i[0]+'/'
                    if i[1]:
                        productTypeInput+=i[1]+'/'
                    productNumInput+=str(i[2])+'/'
                else:
                    material.append([i[5], i[6], i[7]])  # materialCode,materialName,materialNum
            # sum(materialNum) group by materialCode
            materials=select_materialsOfProcurementByCode(procurementCode) # materialCode,materialName,unit,inventoryNum,materialNum,(inventoryNum-materialNum),supplier
            # form data
            addProductForm.productCodeOrType.data = 0
            addProductForm.productCodeOrTypeInput.data=productCodeInput
            addProductForm.productNum.data=productNumInput
            addProductForm.client.data = all_products[0][3]
            if authority[2]=='1' or authority[2]=='2':
                addProductForm.productCodeOrType.render_kw = {"class": "form-control", "readonly": 'true'}
                addProductForm.productCodeOrTypeInput.render_kw = {"class": "form-control", "readonly": 'true'}
                addProductForm.productNum.render_kw = {"class": "form-control", "readonly": 'true'}
                addProductForm.client.render_kw = {"class": "form-control", "readonly": 'true'}
                addProductForm.remark.render_kw = {"class": "form-control", "readonly": 'true'}
                return render_template('procurement.html', form=addProductForm, products=products,materials=materials,productCodeInput=productCodeInput,productTypeInput=productTypeInput,productNumInput=productNumInput,
                                       authority=authority[2], username=username)
            elif authority[2]=='3' or authority[2]=='8':
                return render_template('procurement.html', setting=1, form=addProductForm, products=products,materials=materials,productCodeInput=productCodeInput,productTypeInput=productTypeInput,productNumInput=productNumInput,
                                       authority=authority[2], username=username)
    else:
        return render_template('access_fail.html')