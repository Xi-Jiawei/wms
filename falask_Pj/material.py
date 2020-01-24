from flask import Flask, url_for, render_template, request, redirect, session, Blueprint, jsonify
from datetime import datetime

from db import *
from form import *

#product_managent = Flask(__name__)
material_app=Blueprint('material',__name__)

# xijiawei
# 物料管理
@material_app.route('/material_management', methods=['GET'])
def show_material():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        materials = select_all_materials()
        return render_template('material.html', authority=authority[1], materials=materials, username=username)
    else:
        return render_template('access_fail.html')

# xijiawei
# 更新物料信息
@material_app.route('/update_material', methods=['POST'])
def update_material():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        if request.method == "POST":
            data = request.get_json()
            materialCode = data['materialCode']
            materialType = data['materialType']
            materialName = data['materialName']
            remark = data['remark']
            insertOrUpdate_materialInfo(materialCode, materialType, materialName, remark)
            materials = select_all_materials()
            return jsonify({'materials': materials})
    else:
        return render_template('access_fail.html')

# xijiawei
# 物料管理
@material_app.route('/delete_materials', methods=['POST'])
def delete_materials():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        if request.method == "POST":
            data = request.get_json()
            materialCodeArr = data['materialCodeArr']
            for materialCode in materialCodeArr:
                delete_materialByCode(materialCode)
            materials = select_all_materials()
            return jsonify({'materials': materials})
    else:
        return render_template('access_fail.html')

# xijiawei
# 查看物料出入库记录（显示每个物料的最近3条出入库记录）
@material_app.route('/material_inout_history', methods=['GET', 'POST'])
def material_inout_history():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        if request.method == "GET":
            materialInOut = select_all_materialInOut()
            nowTime = datetime.now().strftime('%Y-%m-%dT%H:%M')
            return render_template('material_inout_history.html', authority=authority[1], materialInOut=materialInOut,
                                   username=username,nowTime=nowTime)
        if request.method == "POST":
            data = request.get_json()
            materialCode = data['materialCode']
            isInOrOut = data['isInOrOut']
            operateNum = data['operateNum']
            unit = data['unit']
            price = data['price']
            supplier = data['supplier']
            documentNumber = data['documentNumber']
            update_materialInOut(documentNumber, isInOrOut, operateNum, unit, price, supplier)
            return jsonify({'ok': True})
    else:
        return render_template('access_fail.html')

# xijiawei
# 查询物料出入库记录
@material_app.route('/material_inout_history_search', methods=['POST'])
def material_inout_history_search():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        if request.method == "POST":
            data = request.get_json()
            startDate = data['startDate']
            endDate = data['endDate']
            materials=select_all_materialInOutFilterByDate(startDate, endDate)
            return jsonify({'materials': materials})
    else:
        return render_template('access_fail.html')

# xijiawei
# 物料管理
@material_app.route('/delete_material_inout', methods=['POST'])
def delete_material_inout():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        if request.method == "POST":
            data = request.get_json()
            documentNumber = data['documentNumber']
            delete_materialInOutByDocNum(documentNumber)
            return jsonify({'ok': True})
    else:
        return render_template('access_fail.html')

# xijiawei
# 物料出入库首页
@material_app.route('/material_inout_index', methods=['GET'])
def material_inout_index():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        if request.method == "GET":
            materials=[]
            materialsInfo = select_all_materials()
            for material in materialsInfo:
                materialInOut = select_materialInOutByCode(material[0])
                if materialInOut:
                    materials.append([material[0], material[1], material[2], material[4], materialInOut[materialInOut.__len__()-1][0], material[5], material[6],materialInOut[materialInOut.__len__()-1][1]])
                else:
                    materials.append([material[0], material[1], material[2], material[4], "", material[5], material[6],""])
            return render_template('material_inout.html', authority=authority[1], materials=materials, username=username)
    else:
        return render_template('access_fail.html')

# xijiawei
# 物料出入库提交
@material_app.route('/material_inout', methods=['POST'])
def material_inout():
    if session.get('username'):
        username = session['username']
        authority = login_Authority(username)
        if request.method == "POST":
            data = request.get_json()
            materialCode = data['materialCode']
            materialName = data['materialName']
            materialType = data['materialType']
            unit = data['unit']
            price = float(data['price'])
            supplier = data['supplier']
            documentNumber = data['documentNumber']
            isInOrOut = int(data['isInOrOut'])
            nowTime = datetime.now()
            operateTime = nowTime.strftime('%Y-%m-%d %H:%M:%S.%f')
            if isInOrOut == 0:
                operateNum = int(data['operateNum'])
            elif isInOrOut == 1:
                operateNum = -int(data['operateNum'])
            else:
                return jsonify({'ok': False})
            insert_materialInOut(documentNumber, materialCode, isInOrOut, operateNum, unit, price, supplier, operateTime, username)
            update_materialInfo(materialCode, materialName, materialType, operateNum, price,unit,supplier)
            return jsonify({'ok': True})
    else:
        return render_template('access_fail.html')

