from flask import Flask, url_for, render_template, request, redirect, session, Blueprint, jsonify
from datetime import datetime
from db import *
from form import *
import time
import json

procurement_app=Blueprint('procurement',__name__)

# xijiawei
#
@procurement_app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test_tablepage.html')

# xijiawei
#
@procurement_app.route('/procurement_history', methods=['GET', 'POST'])
def procurement_history():
    addProductForm = AddProductForm()
    print(session)
    print(session.keys())
    print(session.get('username'))
    if request.method == 'GET':
        if session.get('username'):
            username = session['username']
            authority = login_Authority(username)
            procurementResults = select_procurement() # id,materialCode,materialNum,procurementNum,productCodeStr,productTypeStr,productNumStr,client,entryClerk,entryDate
            procurements = []
            procurement = []
            if len(procurementResults)>0:
                id=procurementResults[0][0]
            for procurementResult in procurementResults:
                if procurementResult[0]!=id:
                    id=procurementResult[0]
                    procurements.append(procurement)
                    procurement = []
                    procurement.append([procurementResult[0], procurementResult[1], procurementResult[2], procurementResult[3],
                         procurementResult[4], procurementResult[5], procurementResult[6], procurementResult[7],
                         procurementResult[8], procurementResult[9]])
                else:
                    procurement.append([procurementResult[0],procurementResult[1],procurementResult[2],procurementResult[3],procurementResult[4],procurementResult[5],procurementResult[6],procurementResult[7],procurementResult[8],procurementResult[9]])
            if len(procurement)>0:
                procurements.append(procurement) # add last procurement
            return render_template('procurement_history.html', form=addProductForm,
                                   procurements=procurements,
                                   authority=authority[2],
                                   username=username)
        else:
            return render_template('access_fail.html')

# xijiawei
#
@procurement_app.route('/delete_procurements', methods=['GET', 'POST'])
def delete_procurements():
    if request.method == "POST":
        data = request.get_json()
        procurementArr = data['procurementArr']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        for procurement in procurementArr:
            id=int(procurement['id'])
            entryDate=procurement['entryDate']
            materials = select_procurementByID(int(id)) # materialCode,materialNum,procurementNum,productCodeStr,productTypeStr,productNumStr,client,remark
            for material in materials:
                materialCode = material[0]
                materialOfInfo = select_materialOfInfo(materialCode) # materialCode, materialName,type,price, department, remainderAmount,supplierFactory
                update_materialOfInfo(materialCode, materialOfInfo[0][5] + material[1] - material[2])
                # materialCode, isInOrOut, price, amount, totalPrice, afterAmount, afterMoney, documentNumber, time
                insert_materialOfInOut(materialCode, 0,materialOfInfo[0][3], material[1] - material[2],(material[1] - material[2])*materialOfInfo[0][3], materialOfInfo[0][5] + material[1] - material[2],
                                       (materialOfInfo[0][5] + material[1] - material[2]) * materialOfInfo[0][3],("pmt-%d" % id), date)
            delete_procurementsByIDAndDate(id,entryDate)
        return jsonify({'ok': True})
    else:
        return jsonify({'ok': False})

# xijiawei
#
@procurement_app.route('/calculate_procurement2', methods=['GET', 'POST'])
def calculate_procurement2():
    if request.method == "POST":
        data = request.get_json()
        productCodeOrTypeInputArr = data['productCodeOrTypeInputArr']
        productCodeOrType = data['productCodeOrType']
        productNumArr = data['productNumArr']
        url=data['url']

        # materials
        materials=[]
        if len(productCodeOrTypeInputArr)>0 and productCodeOrType=="0":
            productCodeArr=productCodeOrTypeInputArr

            # pNumArr
            if len(productNumArr)>len(productCodeArr):
                pNumArr=productNumArr[:len(productCodeArr)]
            else:
                pNumArr = productNumArr
                for i in range(len(productCodeArr)-len(productNumArr)):
                    pNumArr.append("0")

            # 1.checkout productCodeArr[:len(productCodeArr)-2]
            # 2.insert productNum into table materialsOfProduct
            for i in range(len(productCodeArr)-1):
                if not select_productTypeByCode(productCodeArr[i]):
                    return jsonify({'ok': False})
                if (pNumArr[i].isdigit()):
                    update_productNum_materialsOfProduct(productCodeArr[i], int(pNumArr[i]))
                else:
                    update_productNum_materialsOfProduct(productCodeArr[i], 0)
            if (pNumArr[len(productCodeArr)-1].isdigit()):
                update_productNum_materialsOfProduct(productCodeArr[len(productCodeArr)-1], int(pNumArr[len(productCodeArr)-1]))
            else:
                update_productNum_materialsOfProduct(productCodeArr[len(productCodeArr)-1], 0)
            materials=select_materialsOfProduct(productCodeArr) # materials
        elif len(productCodeOrTypeInputArr)>0 and productCodeOrType=="1":
            productTypeArr=productCodeOrTypeInputArr

            # pNumArr
            if len(productNumArr)>len(productTypeArr):
                pNumArr=productNumArr[:len(productTypeArr)]
            else:
                pNumArr = productNumArr
                for i in range(len(productTypeArr)-len(productNumArr)):
                    pNumArr.append("0")

            # 1.checkout productTypeArr[:len(productTypeArr)-2]
            # 2.get productCodeArr by productTypeArr
            # 3.insert productNum into table materialsOfProduct
            productCodeArr=[0 for key in range(len(productTypeArr))]
            for i in range(len(productTypeArr)-1):
                productCode_temp = select_productCodeByType(productTypeArr[i])
                if productCode_temp:
                    productCodeArr[i]=productCode_temp[0][0]
                else:
                    return jsonify({'ok': False})
                if (pNumArr[i].isdigit()):
                    update_productNum_materialsOfProduct(productCodeArr[i], int(pNumArr[i]))
                else:
                    update_productNum_materialsOfProduct(productCodeArr[i], 0)
            productCode_temp=select_productCodeByType(productTypeArr[len(productTypeArr) - 1])
            if productCode_temp:
                productCodeArr[len(productTypeArr)-1] = productCode_temp[0][0]
                if (pNumArr[len(productTypeArr) - 1].isdigit()):
                    update_productNum_materialsOfProduct(productCodeArr[len(productTypeArr) - 1],
                                                         int(pNumArr[len(productTypeArr) - 1]))
                else:
                    update_productNum_materialsOfProduct(productCodeArr[len(productTypeArr) - 1], 0)
            materials=select_materialsOfProduct(productCodeArr) # materials
        else:
            return jsonify({'ok': False})

        # result
        result=[]
        if materials:
            result = [0 for key in range(len(materials))]
            i = 0
            for material in materials:
                materialCode = material[0]
                materialNum = int(material[1])
                remark = "" # remark = material[2]
                if url.find('edit_procurement')==-1:
                    materialInfo = select_materialOfInfo(materialCode)
                else:
                    materialInfo = select_materialOfInfo_temp(materialCode)
                if materialInfo:
                    print("物料信息", materialInfo)
                    stockQuantity = materialInfo[0][5]
                    remainderQuantity = int(stockQuantity) - int(materialNum)
                    if remainderQuantity < 0:
                        result[i] = {'materialCode': materialCode,
                                     'materialName': materialInfo[0][1],
                                     'materialType': materialInfo[0][2],
                                     'department': materialInfo[0][4],
                                     'stockQuantity': materialInfo[0][5],
                                     'materialNum': materialNum,
                                     'remainderQuantity': 0,
                                     'lackQuantity': remainderQuantity,
                                     'supplierFactory': materialInfo[0][6],
                                     'remark': remark}
                    else:
                        result[i] = {'materialCode': materialCode,
                                     'materialName': materialInfo[0][1],
                                     'materialType': materialInfo[0][2],
                                     'department': materialInfo[0][4],
                                     'stockQuantity': materialInfo[0][5],
                                     'materialNum': materialNum,
                                     'remainderQuantity': remainderQuantity,
                                     'lackQuantity': 0,
                                     'supplierFactory': materialInfo[0][6],
                                     'remark': remark}
                else:
                    result[i] = {'materialCode': materialCode,
                                 'exception':("物料库中不存在物料%s！"%materialCode)}
                i += 1
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
#
@procurement_app.route('/procurement', methods=['GET', 'POST'])
def procurement():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        if request.method == "POST":
            # data=request.get_data()
            # data=json.load(request.get_data(as_text=True))
            data = request.get_json()
            productCodeOrTypeInputArr = data['productCodeOrTypeInputArr']
            productCodeOrType = data['productCodeOrType']
            productNumArr = data['productNumArr']
            client = data['client']
            materialArr = data['materialArr']
            if session.get('username'):
                entryClerk = session['username']
            else:
                entryClerk = "unknown"
            id=0
            entryDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

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
            splitStr='/'
            productCodeStr=splitStr.join(productCodeArr)
            productTypeStr=splitStr.join(productTypeArr)
            productNumStr=splitStr.join(productNumArr)

            # id
            maxid = select_maxid_procurement()
            if not maxid[0][0] == None:
                id = int(maxid[0][0]) + 1
            else:
                id = 0

            # material
            for material in materialArr:
                insert_procurement(id, material['materialCode'], int(material['materialNum']), -int(material['lackQuantity']), productCodeStr, productTypeStr,
                                   productNumStr, client, material['remark'], entryClerk, entryDate)
                update_materialOfInfo(material['materialCode'], int(material['remainderQuantity']))
                materialOfInfo = select_materialOfInfo(material['materialCode'])
                if materialOfInfo:
                    insert_materialOfInOut(material['materialCode'], 1, materialOfInfo[0][3],
                                           int(material['stockQuantity']),
                                           int(material['stockQuantity']) * materialOfInfo[0][3],
                                           int(material['remainderQuantity']),
                                           int(material['remainderQuantity'])* materialOfInfo[0][3],
                                           ("pmt-%d"%id),entryDate)
            return jsonify({'ok': True})
        elif request.method == 'GET':
            addProductForm = AddProductForm()
            return render_template('procurement.html', setting=0, form=addProductForm, authority=authority[2],username=username)
    else:
        return render_template('access_fail.html')

# xijiawei
#
@procurement_app.route('/edit_procurement/<id>', methods=['GET', 'POST'])
def edit_procurement(id):
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
            materialArr = data['materialArr']
            if session.get('username'):
                entryClerk = session['username']
            else:
                entryClerk = "unknown"
            entryDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

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
            splitStr='/'
            productCodeStr=splitStr.join(productCodeArr)
            productTypeStr=splitStr.join(productTypeArr)
            productNumStr=splitStr.join(productNumArr)

            # update procurement and update materialOfInfo
            delete_procurementsByID(int(id)) # 清空
            for material in materialArr:
                insert_procurement(int(id), material['materialCode'], int(material['materialNum']), -int(material['lackQuantity']), productCodeStr, productTypeStr,
                                   productNumStr, client, material['remark'], entryClerk, entryDate)
                update_materialOfInfo(material['materialCode'], int(material['remainderQuantity']))
                materialOfInfo = select_materialOfInfo(material['materialCode'])
                if materialOfInfo:
                    insert_materialOfInOut(material['materialCode'], 1, materialOfInfo[0][3],
                                           int(material['stockQuantity']),
                                           int(material['stockQuantity']) * materialOfInfo[0][3],
                                           int(material['remainderQuantity']),
                                           int(material['remainderQuantity'])* materialOfInfo[0][3],
                                           ("pmt-%s"%id),entryDate)
            return jsonify({'ok': True})
        elif request.method == 'GET':

            # return to the status of materialOfInfo before this procurement of id
            copy_materialOfInfo()
            materials = select_procurementByID(int(id)) # materialCode,materialNum,procurementNum,productCodeStr,productTypeStr,productNumStr,client,remark
            procurement = [[0 for key in range(10)] for key in range(len(materials))]
            i=0
            for material in materials:
                materialCode = material[0]
                materialOfInfo = select_materialOfInfo(materialCode) # materialCode, materialName,type,price, department, remainderAmount,supplierFactory
                # if material[2]!=0:
                #     update_materialOfInfo(materialCode, materialOfInfo[0][5] + material[1] - material[2])
                # else:
                #     update_materialOfInfo(materialCode, materialOfInfo[0][5] + material[1])
                update_materialOfInfo_temp(materialCode, materialOfInfo[0][5] + material[1] - material[2])

                # procurement
                procurement[i][0]=material[0] # materialCode
                procurement[i][1]=materialOfInfo[0][1] # materialName
                procurement[i][2]=materialOfInfo[0][2] # materialType
                procurement[i][3]=materialOfInfo[0][4] # department
                procurement[i][4]=materialOfInfo[0][5] + material[1] - material[2] # stockQuantity
                procurement[i][5]=material[1] # materialNum
                procurement[i][6]=materialOfInfo[0][5] # remainderQuantity
                procurement[i][7]=-material[2] # lackQuantity
                procurement[i][8]=materialOfInfo[0][6] # supplierFactory
                procurement[i][9]=material[7] # remark
                i+=1

            # form data
            addProductForm.productCodeOrType.data = 0
            addProductForm.productCodeOrTypeInput.data = materials[0][3]
            addProductForm.productNum.data = materials[0][5]
            addProductForm.client.data = materials[0][6]
            if authority[2]=='1' or authority[2]=='2':
                addProductForm.productCodeOrType.render_kw = {"class": "form-control", "readonly": 'true'}
                addProductForm.productCodeOrTypeInput.render_kw = {"class": "form-control", "readonly": 'true'}
                addProductForm.productNum.render_kw = {"class": "form-control", "readonly": 'true'}
                addProductForm.client.render_kw = {"class": "form-control", "readonly": 'true'}
                return render_template('procurement_view.html', form=addProductForm, procurement=procurement,
                                       authority=authority[2], username=username)
            elif authority[2]=='3' or authority[2]=='8':
                return render_template('procurement.html', setting=1, form=addProductForm, procurement=procurement,
                                       authority=authority[2], username=username)
    else:
        return render_template('access_fail.html')