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
    # addProductForm = AddProductForm()
    # print(session)
    # print(session.keys())
    # print(session.get('username'))
    # if session.get('username'):
    #     username = session['username']
    #     authority = login_Authority(username)
    #     procurementList = select_procurement()
    #     return render_template('procurement.html', form=addProductForm,authority=authority[2], procurementList=procurementList)
    # else:
    #     return render_template('test_fail.html')
    addProductForm = AddProductForm()
    #username = session['username']
    username = '习佳威'
    authority = login_Authority(username)
    procurement_history = select_procurement()
    return render_template('procurement_history.html', form=addProductForm, procurement_history=procurement_history,
                           authority=authority[2])

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
                i += 1
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
                i += 1
        return jsonify({'ok': True, 'result': result})
    else: return jsonify({'ok': -1})

# xijiawei
#
@procurement_app.route('/calculate_procurement2', methods=['GET', 'POST'])
def calculate_procurement2():
    if request.method == "POST":
        data = request.get_json()
        productCodeArr = data['productCodeArr']  # 不要写成productCode=request.data["productcode"]
        productTypeArr = data['productTypeArr']  # 不要写成productCode=request.data["productcode"]
        productNumArr = data['productNumArr']  # 不要写成productCode=request.data["productcode"]
        materials=[]
        if len(productCodeArr)>0 and len(productCodeArr)>len(productTypeArr):
            if len(productNumArr)>len(productCodeArr):
                pNumArr=productNumArr[:len(productCodeArr)]
            else:
                pNumArr = productNumArr
                for i in range(len(productCodeArr)-len(productNumArr)):
                    pNumArr.append("0")
            for i in range(len(productCodeArr)-1):
                # update_productNum_materialsOfProduct(productCodeArr[i], pNumArr[i])
                #if(isinstance(pNumArr[i],int)):
                # time.sleep(0.1) # 防止并发
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
        elif len(productTypeArr)>0 and len(productCodeArr)<len(productTypeArr):
            if len(productNumArr)>len(productTypeArr):
                pNumArr=productNumArr[:len(productTypeArr)]
            else:
                pNumArr = productNumArr
                for i in range(len(productTypeArr)-len(productNumArr)):
                    pNumArr.append("0")
            productCodeArr=[0 for key in range(len(productTypeArr))]
            for i in range(len(productTypeArr)-1):
                # time.sleep(0.1)
                # if not select_productCodeByType(productTypeArr[i]):
                #     return jsonify({'ok': False})
                # productCodeArr[i]=select_productCodeByType(productTypeArr[i])
                productCode_temp = select_productCodeByType(productTypeArr[i])
                if productCode_temp:
                    productCodeArr[i]=productCode_temp[0][0]
                else:
                    return jsonify({'ok': False})
                if (pNumArr[i].isdigit()):
                    update_productNum_materialsOfProduct(productCodeArr[i], int(pNumArr[i]))
                else:
                    update_productNum_materialsOfProduct(productCodeArr[i], 0)
            # time.sleep(0.1)
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
            if len(productNumArr)>len(productCodeArr):
                pNumArr=productNumArr[:len(productCodeArr)]
            else:
                pNumArr = productNumArr
                for i in range(len(productCodeArr)-len(productNumArr)):
                    pNumArr.append("0")
            for i in range(len(productCodeArr)-1):
                # update_productNum_materialsOfProduct(productCodeArr[i], pNumArr[i])
                #if(isinstance(pNumArr[i],int)):
                # time.sleep(0.1) # 防止并发
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
        print("采购物料",materials)
        result=[0 for key in range(len(materials))]
        i=0
        for material in materials:
            materialCode = material[0]
            materialNum = int(material[1])
            remark = material[2]
            materialInfo = select_materialOfInfo(materialCode)
            print("物料信息",materialInfo)
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
    # addProductForm = AddProductForm()
    # print(session)
    # print(session.keys())
    # print(session.get('username'))
    # if session.get('username'):
    #     username = session['username']
    #     authority = login_Authority(username)
    #     procurementList = select_procurement()
    #     return render_template('procurement.html', form=addProductForm,authority=authority[2], procurementList=procurementList)
    # else:
    #     return render_template('test_fail.html')
    #if addProductForm.validate_on_submit():
    if request.method=="POST":
        # data=request.get_data()
        #data=json.load(request.get_data(as_text=True))
        data=request.get_json()
        productCodeArr=data['productCodeArr']
        productTypeArr=data['productTypeArr']
        productNumArr=data['productNumArr']
        client=data['client']
        materialArr=data['materialArr']
        if session.get('username'):
            entryClerk=session['username']
        else:
            entryClerk="未知"
        entryDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        if len(productCodeArr)>0:
            for i in range(len(productCodeArr)):
                productType = select_productTypeByCode(productCodeArr[i])
                insert_procurement(productCodeArr[i], productType[0][0], int(productNumArr[i]), client, entryClerk,
                                   entryDate)
        else:
            for i in range(len(productTypeArr)):
                productCode = select_productCodeByType(productTypeArr[i])
                insert_procurement(productCode[0][0], productTypeArr[i], int(productNumArr[i]), client, entryClerk,
                                   entryDate)
        for material in materialArr:
            print(material['materialCode'])
            print(int(material['remainderAmount']))
            update_materialOfInfo(material['materialCode'], int(material['remainderAmount']))
            materialOfInfo = select_materialOfInfo(material['materialCode'])
            insert_materialOfInOut(material['materialCode'], '出库', int(material['materialAmount']),
                                   int(material['remainderAmount']),
                                   int(material['remainderAmount']) * materialOfInfo[0][3])
        return jsonify({'ok': True})
    elif request.method=='GET':
        addProductForm = AddProductForm()
        return render_template('procurement.html', form=addProductForm)