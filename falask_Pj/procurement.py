from flask import Flask, url_for, render_template, request, redirect, session, Blueprint, jsonify
from datetime import datetime
from db import *
from form import *
import time
import json

procurement_app=Blueprint('procurement',__name__)

# xijiawei
# 成品管理
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
            procurementResult = select_procurement()
            procurement_history = [[0 for key in range(7)] for key in range(len(procurementResult))]
            for i in range(len(procurementResult)):
                procurement_history[i][0] = procurementResult[i][0]
                procurement_history[i][1] = procurementResult[i][1].replace(',', '/')
                procurement_history[i][2] = procurementResult[i][2].replace(',', '/')
                procurement_history[i][3] = procurementResult[i][3].replace(',', '/')
                # procurement_history[i][4] = procurementResult[i][4][:procurementResult[i][4].index(',')]
                # procurement_history[i][5] = procurementResult[i][5][:procurementResult[i][5].index(',')]
                # procurement_history[i][6] = procurementResult[i][6][:procurementResult[i][6].index(',')]
                if not procurementResult[i][4].find(',') == -1:
                    procurement_history[i][4] = procurementResult[i][4][:procurementResult[i][4].find(',')]
                else:
                    procurement_history[i][4] = procurementResult[i][4]
                if not procurementResult[i][5].find(',') == -1:
                    procurement_history[i][5] = procurementResult[i][5][:procurementResult[i][5].find(',')]
                else:
                    procurement_history[i][5] = procurementResult[i][5]
                if not procurementResult[i][6].find(',') == -1:
                    procurement_history[i][6] = procurementResult[i][6][:procurementResult[i][6].find(',')]
                else:
                    procurement_history[i][6] = procurementResult[i][6]
            return render_template('procurement_history.html', form=addProductForm,
                                   procurement_history=procurement_history,
                                   authority=authority[2],
                                   username=username)
        else:
            return render_template('test_fail.html')

# xijiawei
# 成品管理
@procurement_app.route('/delete_procurements', methods=['GET', 'POST'])
def delete_procurements():
    if request.method == "POST":
        data = request.get_json()
        procurementArr = data['procurementArr']
        for procurement in procurementArr:
            id=int(procurement['id'])
            entryDate=procurement['entryDate']
            productResult=select_procurementByID(id)
            # productCodeArr = productResult[0, :]
            # productCodeArr = productResult[:, 0]
            productCodeArr = [0 for key in range(len(productResult))]
            i=0
            for product in productResult:
                productCode= product[0]
                productNum = product[1]
                update_productNum_materialsOfProduct(productCode,productNum)
                productCodeArr[i]=productCode
                i+=1
            materials=select_materialsOfProduct(productCodeArr)
            for material in materials:
                materialCode = material[0]
                materialNum = int(material[1])
                remark = material[2]
                materialInfo = select_materialOfInfo(materialCode)
                if materialInfo:
                    stockQuantity = materialInfo[0][5]
                    remainderQuantity = int(stockQuantity) + int(materialNum)  # 取消采购，相当于物料重新入库
                    update_materialOfInfo(materialCode, remainderQuantity)
                    insert_materialOfInOut(materialCode, ('取消采购，代号：%d' % id), materialNum, remainderQuantity,
                                           remainderQuantity * materialInfo[0][3])
            delete_procurementsByIDAndDate(id,entryDate)
        return jsonify({'ok': True})
    else:
        return jsonify({'ok': False})

# xijiawei
# 成品管理
@procurement_app.route('/calculate_procurement', methods=['GET', 'POST'])
def calculate_procurement():
    if request.method == "POST":
        data = request.get_json()
        productCodeArr = data['productCodeArr']  # 不要写成productCode=request.data["productcode"]
        productTypeArr = data['productTypeArr']  # 不要写成productCode=request.data["productcode"]
        productNumArr = data['productNumArr']  # 不要写成productCode=request.data["productcode"]
        if len(productCodeArr)>0:
            if len(productNumArr)>len(productCodeArr):
                pNumArr=productNumArr[:len(productCodeArr)]
            else:
                pNumArr = productNumArr
                for i in range(len(productCodeArr)-len(productNumArr)):
                    pNumArr.append("0")
            for i in range(len(productCodeArr)):
                # update_productNum_materialsOfProduct(productCodeArr[i], pNumArr[i])
                #if(isinstance(pNumArr[i],int)):
                if not select_productTypeByCode(productCodeArr[i]):
                    return jsonify({'ok': False})
                if (pNumArr[i].isdigit()):
                    update_productNum_materialsOfProduct(productCodeArr[i], int(pNumArr[i]))
                else:
                    update_productNum_materialsOfProduct(productCodeArr[i], 0)
            materials=select_materialsOfProduct(productCodeArr)
        else:
            if len(productNumArr)>len(productTypeArr):
                pNumArr=productNumArr[:len(productTypeArr)]
            else:
                pNumArr = productNumArr
                for i in range(len(productTypeArr)-len(productNumArr)):
                    pNumArr.append("0")
            productCodeArr=[0 for key in range(len(productTypeArr))]
            for i in range(len(productTypeArr)):
                # productCodeArr[i]=select_productCodeByType(productTypeArr[i])
                productCode_temp = select_productCodeByType(productTypeArr[i])
                if productCode_temp:
                    productCodeArr[i] = productCode_temp
                else:
                    return jsonify({'ok': False})
                # update_productNum_materialsOfProduct(productCodeArr[i], pNumArr[i])
                # if(isinstance(pNumArr[i],int)):
                if (pNumArr[i].isdigit()):
                    update_productNum_materialsOfProduct(productCodeArr[i], int(pNumArr[i]))
                else:
                    update_productNum_materialsOfProduct(productCodeArr[i], 0)
            materials=select_materialsOfProduct(productTypeArr)
        result=[0 for key in range(len(materials))]
        i=0
        for material in materials:
            materialCode = material[0]
            materialNum = int(material[1])
            remark = material[2]
            materialInfo = select_materialOfInfo(materialCode)
            if materialInfo:
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
                    # materialCode,sum(materialNum),remark
                    # materialCode, materialName,type,price, department, remainderAmount,supplierFactory
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
                             'exception': ("物料库中不存在物料%s！" % materialCode)}
            i+=1
        return jsonify({'ok': True, 'result': result})
    else: return jsonify({'ok': -1})

# xijiawei
#
@procurement_app.route('/calculate_procurement2', methods=['GET', 'POST'])
def calculate_procurement2():
    if request.method == "POST":
        data = request.get_json()
        # productCodeArr = data['productCodeArr']  # 不要写成productCode=request.data["productcode"]
        # productTypeArr = data['productTypeArr']  # 不要写成productCode=request.data["productcode"]
        # productNumArr = data['productNumArr']  # 不要写成productCode=request.data["productcode"]
        productCodeOrTypeInput = data['productCodeOrTypeInput']
        productCodeOrType = data['productCodeOrType']
        productNumArr = data['productNumArr']
        materials=[]
        if len(productCodeOrTypeInput)>0 and productCodeOrType=="0":
            productCodeArr=productCodeOrTypeInput
            if len(productNumArr)>len(productCodeArr):
                pNumArr=productNumArr[:len(productCodeArr)]
            else:
                pNumArr = productNumArr
                for i in range(len(productCodeArr)-len(productNumArr)):
                    pNumArr.append("0")
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
            materials=select_materialsOfProduct(productCodeArr)
        elif len(productCodeOrTypeInput)>0 and productCodeOrType=="1":
            productTypeArr=productCodeOrTypeInput
            if len(productNumArr)>len(productTypeArr):
                pNumArr=productNumArr[:len(productTypeArr)]
            else:
                pNumArr = productNumArr
                for i in range(len(productTypeArr)-len(productNumArr)):
                    pNumArr.append("0")
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
            materials=select_materialsOfProduct(productCodeArr)
        else:
            return jsonify({'ok': False})
        print("采购物料",materials)
        result=[]
        if materials:
            result = [0 for key in range(len(materials))]
            i = 0
            for material in materials:
                materialCode = material[0]
                materialNum = int(material[1])
                remark = material[2]
                materialInfo = select_materialOfInfo(materialCode)
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
            productCodeOrTypeInput = data['productCodeOrTypeInput']
            productCodeOrType = data['productCodeOrType']
            productNumArr = data['productNumArr']
            client = data['client']
            materialArr = data['materialArr']
            if session.get('username'):
                entryClerk = session['username']
            else:
                entryClerk = "admin"
            entryDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            if productCodeOrType == "0":
                productCodeArr = productCodeOrTypeInput
                if not select_productTypeByCode(productCodeArr[len(productCodeArr) - 1]):
                    return jsonify({'ok': False})
                else:
                    maxid = select_maxid_procurement()
                    if not maxid[0][0] == None:
                        id = int(maxid[0][0]) + 1
                    else:
                        id = 0
                    for i in range(len(productCodeArr)):
                        productType = select_productTypeByCode(productCodeArr[i])
                        insert_procurement(id, productCodeArr[i], productType[0][0], int(productNumArr[i]), client,
                                           entryClerk,
                                           entryDate)
            elif productCodeOrType == "1":
                productTypeArr = productCodeOrTypeInput
                if not select_productCodeByType(productTypeArr[len(productTypeArr) - 1]):
                    return jsonify({'ok': False})
                else:
                    maxid = select_maxid_procurement()
                    if not maxid[0][0] == None:
                        id = int(maxid[0][0]) + 1
                    else:
                        id = 0
                    for i in range(len(productTypeArr)):
                        productCode = select_productCodeByType(productTypeArr[i])
                        insert_procurement(id, productCode[0][0], productTypeArr[i], int(productNumArr[i]), client,
                                           entryClerk,
                                           entryDate)
            for material in materialArr:
                print(material['materialCode'])
                print(int(material['remainderAmount']))
                update_materialOfInfo(material['materialCode'], int(material['remainderAmount']))
                materialOfInfo = select_materialOfInfo(material['materialCode'])
                if materialOfInfo:
                    insert_materialOfInOut(material['materialCode'], '出库', int(material['materialAmount']),
                                           int(material['remainderAmount']),
                                           int(material['remainderAmount']) * materialOfInfo[0][3])
            return jsonify({'ok': True})
        elif request.method == 'GET':
            addProductForm = AddProductForm()
            return render_template('procurement.html', setting=0, form=addProductForm, authority=authority[2],username=username)
    else:
        return render_template('test_fail.html')

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
        if request.method == "POST":
            data = request.get_json()
            productCodeOrTypeInput = data['productCodeOrTypeInput']
            productCodeOrType = data['productCodeOrType']
            productNumArr = data['productNumArr']
            client = data['client']
            materialArr = data['materialArr']
            if session.get('username'):
                entryClerk = session['username']
            else:
                entryClerk = "admin"
            entryDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            delete_procurementsByID(int(id)) # 清空
            if productCodeOrType == "0":
                productCodeArr = productCodeOrTypeInput
                if not select_productTypeByCode(productCodeArr[len(productCodeArr) - 1]):
                    return jsonify({'ok': False})
                else:
                    for i in range(len(productCodeArr)):
                        productType = select_productTypeByCode(productCodeArr[i])
                        # update_procurement(id, productCodeArr[i], productType[0][0], int(productNumArr[i]), client,
                        #                    entryClerk,
                        #                    entryDate)
                        insert_procurement(int(id), productCodeArr[i], productType[0][0], int(productNumArr[i]), client,
                                           entryClerk,
                                           entryDate)
            elif productCodeOrType == "1":
                productTypeArr = productCodeOrTypeInput
                if not select_productCodeByType(productTypeArr[len(productTypeArr) - 1]):
                    return jsonify({'ok': False})
                else:
                    for i in range(len(productTypeArr)):
                        productCode = select_productCodeByType(productTypeArr[i])
                        # update_procurement(id, productCode[0][0], productTypeArr[i], int(productNumArr[i]), client,
                        #                    entryClerk,
                        #                    entryDate)
                        insert_procurement(int(id), productCode[0][0], productTypeArr[i], int(productNumArr[i]), client,
                                           entryClerk,
                                           entryDate)
            for material in materialArr:
                print(material['materialCode'])
                print(int(material['remainderAmount']))
                update_materialOfInfo(material['materialCode'], int(material['remainderAmount'])) # 更新物料静态库
                materialOfInfo = select_materialOfInfo(material['materialCode'])
                if materialOfInfo:
                    # 插入物料出入库记录
                    insert_materialOfInOut(material['materialCode'], '采购更新', int(material['materialAmount']),
                                           int(material['remainderAmount']),
                                           int(material['remainderAmount']) * materialOfInfo[0][3])
            return jsonify({'ok': True})
        elif request.method == 'GET':
            productResult=select_procurementByID(int(id))
            productCodeArr = [0 for key in range(len(productResult))]
            productCodeStr=''
            productTypeStr=''
            productNumStr=''
            i=0
            for product in productResult:
                productCode= product[0]
                productNum = product[1]
                productType = product[2]
                client = product[3]
                productCodeArr[i]=productCode
                productCodeStr+='/'+productCode
                productTypeStr+='/'+productType
                productNumStr+='/'+str(productNum)
                i+=1
            materials=select_materialsOfProduct(productCodeArr)
            procurement=[[0 for key in range(10)] for key in range(len(materials))]
            i=0
            for material in materials:
                materialCode = material[0]
                materialNum = int(material[1])
                remark = material[2]
                materialInfo = select_materialOfInfo(materialCode)
                stockQuantity = materialInfo[0][5]
                remainderQuantity = int(stockQuantity) - int(materialNum)
                if remainderQuantity < 0:
                    procurement[i][0]=materialCode
                    procurement[i][1] = materialInfo[0][1]
                    procurement[i][2]=materialInfo[0][2]
                    procurement[i][3]=materialInfo[0][4]
                    procurement[i][4]=materialInfo[0][5]
                    procurement[i][5]=materialNum
                    procurement[i][6]=0
                    procurement[i][7]=remainderQuantity
                    procurement[i][8]=materialInfo[0][6]
                    procurement[i][9]=remark
                else:
                    procurement[i][0] = materialCode
                    procurement[i][1] = materialInfo[0][1]
                    procurement[i][2] = materialInfo[0][2]
                    procurement[i][3] = materialInfo[0][4]
                    procurement[i][4] = materialInfo[0][5]
                    procurement[i][5] = materialNum
                    procurement[i][6] = remainderQuantity
                    procurement[i][7] = 0
                    procurement[i][8] = materialInfo[0][6]
                    procurement[i][9] = remark
                i+=1
            addProductForm.productCodeOrType.data = 0
            addProductForm.productCodeOrTypeInput.data = productCodeStr[1:]
            addProductForm.productNum.data = productNumStr[1:]
            addProductForm.client.data = client
            return render_template('procurement.html', setting=1,form=addProductForm,procurement=procurement, authority=authority[2],username=username)
    else:
        return render_template('test_fail.html')