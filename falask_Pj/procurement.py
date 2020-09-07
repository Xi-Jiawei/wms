from flask import render_template, request, session, Blueprint, jsonify

from db import *
from form import *

procurement_app=Blueprint('procurement',__name__)

# xijiawei
# 采购记录
@procurement_app.route('/procurement_history', methods=['GET'])
def procurement_history():
    form = ProductForm()
    print(session)
    print(session.keys())
    print(session.get('username'))
    if request.method == 'GET':
        if session.get('username'):
            username = session['username']
            authority = select_user_authority(username)
            all_procurements = select_procurement() # count(p.procurementCode),procurementCode,productCode,materialCodeConcatStr,materialNameConcatStr,materialNumConcatStr,productType,productNum,client,entryClerk,entryDate
            procurements=[]
            procurementCode=''
            if all_procurements:
                for i in all_procurements:
                    if not i[1] == procurementCode:
                        procurementCode = i[1]
                        procurement = []
                        product = []
                        procurements.append(procurement)
                        procurement.append(i[0])  # count(p.procurementCode)
                        procurement.append(i[1])  # procurementCode
                        product.append([i[2], i[6], i[7], i[3], i[4], i[
                            5]])  # productCode,productType,productNum,materialCodeConcatStr,materialNameConcatStr,materialNumConcatStr
                        procurement.append(product)
                        procurement.append(i[8])  # client
                        procurement.append(i[9])  # entryClerk
                        procurement.append(i[10].strftime('%Y-%m-%d %H:%M:%S.%f')[0:21])  # entryDate
                    else:
                        product.append([i[2], i[6], i[7], i[3], i[4], i[5]])
            return render_template('procurement_history.html', form=form,
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
        username = data['username']
        for procurementCode in procurementCodeArr:
            # delete_procurementByCode(procurementCode, username)
            myThread(target=delete_procurementByCode, args=(procurementCode, username,))
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
                # result = select_productTypeByCode(productCode)
                thread = myThread(target=select_productTypeByCode, args=(productCode,))
                result = thread.get_result()
                if result:
                    productTypeArr.append(result[0][0])
                else:
                    return jsonify({'ok': False})
            # result = select_productTypeByCode(productCodeArr[len(productCodeArr) - 1])
            thread = myThread(target=select_productTypeByCode, args=(productCodeArr[len(productCodeArr) - 1],))
            result = thread.get_result()
            if result:
                productTypeArr.append(result[0][0])
            else:
                productCodeArr.pop(len(productCodeArr) - 1)
        elif productCodeOrType == "1":
            productTypeArr = productCodeOrTypeInputArr
            # productTypeArrTemp=productTypeArr[0:len(productTypeArr) - 1]
            for productType in productTypeArr[0:len(productTypeArr) - 1]:
                # result = select_productCodeByType(productType)
                thread = myThread(target=select_productCodeByType, args=(productType,))
                result = thread.get_result()
                if result:
                    # productCodeArr.append(select_productCodeByType(productType)[0][0])
                    productCodeArr.append(result[0][0])
                else:
                    return jsonify({'ok': False})
            # result = select_productCodeByType(productTypeArr[len(productTypeArr) - 1])
            thread = myThread(target=select_productCodeByType, args=(productTypeArr[len(productTypeArr) - 1],))
            result = thread.get_result()
            if result:
                # productCodeArr.append(select_productCodeByType(productTypeArr[len(productTypeArr) - 1])[0][0])
                productCodeArr.append(result[0][0])
            else:
                productTypeArr.pop(len(productTypeArr) - 1)

        # productNum
        if len(productNumArr)<len(productCodeArr):
            for i in range(len(productCodeArr)-len(productNumArr)):
                productNumArr.append(0)

        # materials
        products = []
        for i in range(productCodeArr.__len__()):
            # materialsOfProduct = select_materialsOfProductByCode(productCodeArr[i])  # materialCode,materialName,materialType,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost
            thread = myThread(target=select_materialsOfProductByCode, args=(productCodeArr[i],))
            materialsOfProduct = thread.get_result()
            # productInfo = select_productInfoByCode(productCodeArr[i])  # productType,client,uint,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk
            thread = myThread(target=select_productInfoByCode, args=(productCodeArr[i],))
            productInfo = thread.get_result()
            product = []
            material = []
            product.append(productCodeArr[i])
            product.append(productInfo[0][0])
            product.append(productNumArr[i])
            for materialOfProduct in materialsOfProduct:
                materialInfo = select_materialInfoByCode(materialOfProduct[0])  # materialName,materialType,remark,inventoryNum,price,inventoryMoney,supplier
                material.append([materialOfProduct[0], materialInfo[0][0], materialInfo[0][1], materialOfProduct[3]])
            product.append(material)
            # productCode,productType,productNum,[materialCode,materialName,materialType,materialNum]
            products.append(product)
            # update_productNumOfProductInfo(productCodeArr[i], productNumArr[i]) # 更新productNum字段，以便采购时进行物料汇总计算
            myThread(target=update_productNumOfProductInfo, args=(productCodeArr[i], productNumArr[i],))
        # materials=select_materialsOfProductByCodeArr(productCodeArr) # materialCode,materialName,materialType,unit,inventoryNum,materialNum,(inventoryNum-materialNum),supplier
        thread = myThread(target=select_materialsOfProductByCodeArr, args=(productCodeArr,))
        materials = thread.get_result()
        result={'products':products,'materials':materials}
        return jsonify({'ok': True, 'result': result})
    else: return jsonify({'ok': -1})

# xijiawei
# 根据产品编码查询产品型号
@procurement_app.route('/productTypeByCode', methods=['GET', 'POST'])
def productTypeByCode():
    if request.method == "POST":
        data = request.get_json()
        productCodeArr = data['productCodeArr']  # 不要写成productCode=request.data["productcode"]
        productTypeArrStr=""
        for productCode in productCodeArr:
            # result = select_productTypeByCode(productCode)
            thread = myThread(target=select_productTypeByCode, args=(productCode,))
            result = thread.get_result()
            if result:
                productTypeArrStr+=result[0][0]+"/"
        return jsonify({'ok': True, 'productTypeArrStr': productTypeArrStr})
    else: return jsonify({'ok': -1})

# xijiawei
# 根据产品型号查询产品编码
@procurement_app.route('/productCodeByType', methods=['GET', 'POST'])
def productCodeByType():
    if request.method == "POST":
        data = request.get_json()
        productTypeArr = data['productTypeArr']  # 不要写成productCode=request.data["productcode"]
        productCodeArrStr = ""
        for productType in productTypeArr:
            # result = select_productCodeByType(productType)
            thread = myThread(target=select_productCodeByType, args=(productType,))
            result = thread.get_result()
            if result:
                productCodeArrStr += result[0][0] + "/"
        return jsonify({'ok': True, 'productCodeArrStr': productCodeArrStr})
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
        authority = select_user_authority(username)
        if request.method == "POST":
            data = request.get_json()
            productCodeOrTypeInputArr = data['productCodeOrTypeInputArr']
            productCodeOrType = data['productCodeOrType']
            productNumArr = data['productNumArr']
            client = data['client']
            remarkArr = data['remarkArr']
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
                # result = select_productTypeByCode(productCodeArr[len(productCodeArr) - 1])
                thread = myThread(target=select_productTypeByCode, args=(productCodeArr[len(productCodeArr) - 1],))
                result = thread.get_result()
                if not result:
                    return jsonify({'ok': False})
                else:
                    for productCode in productCodeArr:
                        # productTypeArr.append(select_productTypeByCode(productCode)[0][0])
                        thread = myThread(target=select_productTypeByCode, args=(productCode,))
                        result = thread.get_result()
                        productTypeArr.append(result[0][0])
            elif productCodeOrType == "1":
                productTypeArr = productCodeOrTypeInputArr
                # result = select_productCodeByType(productTypeArr[len(productTypeArr) - 1])
                thread = myThread(target=select_productCodeByType, args=(productTypeArr[len(productTypeArr) - 1],))
                result = thread.get_result()
                if not result:
                    return jsonify({'ok': False})
                else:
                    for productType in productTypeArr:
                        # productCodeArr.append(select_productCodeByType(productType)[0][0])
                        thread = myThread(target=select_productCodeByType, args=(productType,))
                        result = thread.get_result()
                        productCodeArr.append(result[0][0])

            # procurementCode=uuid.uuid1() # 使用uuid生成唯一代号
            procurementCode=datetime.now().strftime('%Y%m%d%H%M%S%f') # 使用时间戳生成唯一代号
            procurementCode="PM"+procurementCode[0:16] # 使用时间戳生成唯一代号
            # insert_procurement(procurementCode, productCodeArr, productNumArr, client, remarkArr, entryClerk, entryTime)
            myThread(target=insert_procurement, args=(procurementCode, productCodeArr, productNumArr, client, remarkArr, entryClerk, entryTime,))
            return jsonify({'ok': True})
        elif request.method == 'GET':
            form = ProductForm()
            return render_template('procurement.html', setting=0, form=form, authority=authority[2],username=username)
    else:
        return render_template('access_fail.html')

# xijiawei
# 修改采购
@procurement_app.route('/edit_procurement/<procurementCode>', methods=['GET', 'POST'])
def edit_procurement(procurementCode):
    print(session)
    print(session.keys())
    print(session.get('username'))
    form = ProductForm()
    if session.get('username'):
        username = session['username']
        authority = select_user_authority(username)

        # POST
        if request.method == "POST":
            data = request.get_json()
            productCodeOrTypeInputArr = data['productCodeOrTypeInputArr']
            productCodeOrType = data['productCodeOrType']
            productNumArr = data['productNumArr']
            client = data['client']
            remarkArr = data['remarkArr']
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
                # result = select_productTypeByCode(productCodeArr[len(productCodeArr) - 1])
                thread = myThread(target=select_productTypeByCode, args=(productCodeArr[len(productCodeArr) - 1],))
                result = thread.get_result()
                if not result:
                    return jsonify({'ok': False})
                else:
                    for i in range(len(productCodeArr)):
                        # productType = select_productTypeByCode(productCodeArr[i])
                        thread = myThread(target=select_productTypeByCode, args=(productCodeArr[i],))
                        productType = thread.get_result()
                        productTypeArr[i]=productType[0][0]
            elif productCodeOrType == "1":
                productTypeArr = productCodeOrTypeInputArr
                # result = select_productCodeByType(productTypeArr[len(productTypeArr) - 1])
                thread = myThread(target=select_productCodeByType, args=(productTypeArr[len(productTypeArr) - 1],))
                result = thread.get_result()
                if not result:
                    return jsonify({'ok': False})
                else:
                    for i in range(len(productTypeArr)):
                        # productCode = select_productCodeByType(productTypeArr[i])
                        thread = myThread(target=select_productCodeByType, args=(productTypeArr[i],))
                        productCode = thread.get_result()
                        productCodeArr[i] = productCode[0][0]

            # 复杂方式：判断更新的采购是否修改了产品编码，如果只是修改数量，则只在内部更新出入库
            # productCodeArrOld=[]
            # result=select_procurementByCode(procurementCode)
            # for i in result:
            #     productCodeArrOld.append(i[0])
            # # 判断更新的采购是否修改了产品编码
            # if list(set(productCodeArr).difference(set(productCodeArrOld)))==[]:
            #     update_procurement(procurementCode, productCodeArr, productNumArr, client, remarkArr, entryClerk, entryTime)
            # else:
            #     # update procurement and update materialInfo
            #     delete_procurementByCode(procurementCode)  # 撤回上次采购
            #     # insert_procurement(procurementCode, productCodeArr, productNumArr, client, remarkArr, entryClerk, entryTime)
            #     insert_procurement(procurementCode, productCodeArr, productNumArr, client, remarkArr, "系统账号", entryTime)
            # update procurement and update materialInfo
            # 简单方式：无论是否修改了产品编码，都是先撤回上次采，再插入新采购
            # delete_procurementByCode(procurementCode, entryClerk)  # 撤回上次采购
            myThread(target=delete_procurementByCode, args=(procurementCode, entryClerk,))
            # insert_procurement(procurementCode, productCodeArr, productNumArr, client, remarkArr, entryClerk, entryTime)
            myThread(target=insert_procurement, args=(procurementCode, productCodeArr, productNumArr, client, remarkArr, entryClerk, entryTime,))
            return jsonify({'ok': True})
        elif request.method == 'GET':
            all_products = select_procurementByCode(procurementCode) # productCode,productType,productNum,client,remark,materialCode,materialName,materialType,materialNum
            products = []
            productCode = ''
            productCodeInput = ''
            productTypeInput = ''
            productNumInput = ''
            for i in all_products:
                # print("productCode: " + i[0] + "; materialCode: " + i[5])
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
                    if i[5] and i[6] and i[7] and i[8]:
                        material.append([i[5], i[6], i[7], i[8]])  # materialCode,materialName,materialType,materialNum
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
                    material.append([i[5], i[6], i[7], i[8]])  # materialCode,materialName,materialType,materialNum
            # sum(materialNum) group by materialCode
            materials=select_materialsOfProcurementByCode(procurementCode) # materialCode,materialName,materialType,unit,inventoryNum,materialNum,(inventoryNum-materialNum),supplier
            # for i in materials:
            #     print("materialCode: " + i[0])
            # form data
            form.productCodeOrType.data = 0
            form.productCodeOrTypeInput.data=productCodeInput
            form.productNum.data=productNumInput
            form.client.data = all_products[0][3]
            if authority[2]=='1' or authority[2]=='2':
                form.productCodeOrType.render_kw = {"class": "form-control", "readonly": 'true'}
                form.productCodeOrTypeInput.render_kw = {"class": "form-control", "readonly": 'true'}
                form.productNum.render_kw = {"class": "form-control", "readonly": 'true'}
                form.client.render_kw = {"class": "form-control", "readonly": 'true'}
                form.remark.render_kw = {"class": "form-control", "readonly": 'true'}
                return render_template('procurement.html', form=form, products=products,materials=materials,productCodeInput=productCodeInput,productTypeInput=productTypeInput,productNumInput=productNumInput,
                                       authority=authority[2], username=username)
            elif authority[2]=='3' or authority[2]=='8':
                form.productCodeOrType.render_kw = {"class": "form-control", "readonly": 'true'}
                form.productCodeOrTypeInput.render_kw = {"class": "form-control", "readonly": 'true'}
                form.productNum.render_kw = {"class": "form-control", "readonly": 'true'}
                form.client.render_kw = {"class": "form-control", "readonly": 'true'}
                form.remark.render_kw = {"class": "form-control", "readonly": 'true'}
                return render_template('procurement.html', setting=1, form=form, products=products,materials=materials,productCodeInput=productCodeInput,productTypeInput=productTypeInput,productNumInput=productNumInput,
                                       authority=authority[2], username=username)
    else:
        return render_template('access_fail.html')