from flask import render_template, request, session, Blueprint, jsonify

from db import *
from form import *

from datetime import datetime

#material_app = Flask(__name__)
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
        # authority = select_user_authority(username)
        thread = myThread(target=select_user_authority, args=(username,))
        authority = thread.get_result()
        # materials = select_all_materials()
        thread = myThread(target=select_all_materials,args=())
        materials = thread.get_result()
        return render_template('material.html', authority=authority[0], materials=materials, username=username)
    else:
        return render_template('access_fail.html')

# xijiawei
# 添加或更新物料信息
@material_app.route('/update_material', methods=['POST'])
def update_material():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        if request.method == "POST":
            data = request.get_json()
            materialCode = data['materialCode']
            materialType = data['materialType']
            materialName = data['materialName']
            remark = data['remark']
            # insertOrUpdate_materialInfo(materialCode, materialType, materialName, remark)
            myThread(target=insertOrUpdate_materialInfo, args=(materialCode, materialType, materialName, remark,))
            # materials = select_all_materials()
            thread = myThread(target=select_all_materials, args=())
            materials = thread.get_result()
            return jsonify({'materials': materials})
    else:
        return jsonify({'ok': False})

# xijiawei
# 删除物料
@material_app.route('/delete_materials', methods=['POST'])
def delete_materials():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        if request.method == "POST":
            data = request.get_json()
            materialCodeArr = data['materialCodeArr']
            for materialCode in materialCodeArr:
                # delete_materialByCode(materialCode)
                myThread(target=delete_materialByCode, args=(materialCode,))
            # materials = select_all_materials()
            thread = myThread(target=select_all_materials, args=())
            materials = thread.get_result()
            return jsonify({'materials': materials})
    else:
        return jsonify({'ok': False})

# xijiawei
# 物料出入库
@material_app.route('/material_inout', methods=['GET', 'POST'])
def material_inout():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        username = session['username']
        # authority = select_user_authority(username)
        thread = myThread(target=select_user_authority, args=(username,))
        authority = thread.get_result()
        if request.method == "GET":
            # materials = select_all_materials() # materialCode,materialName,materialType,inventoryNum,unit,price,inventoryMoney,supplier,remark
            thread = myThread(target=select_all_materials, args=())
            materials = thread.get_result()
            # inventoryMoneySum = select_sum_materials()
            thread = myThread(target=select_sum_materials, args=())
            inventoryMoneySum = thread.get_result()
            nowTime = datetime.now().strftime('%Y-%m-%d')
            return render_template('material_inout.html', authority=authority[0], materials=materials, inventoryMoneySum=inventoryMoneySum[0][0], username=username, nowTime=nowTime)
        if request.method == "POST":
            data = request.get_json()
            materialCode = data['materialCode']
            materialName = data['materialName']
            materialType = data['materialType']
            unit = data['unit']
            price = float(data['price'])
            supplier = data['supplier']
            isInOrOut = int(data['isInOrOut'])
            if not (isInOrOut == 0 or isInOrOut == 1):
                return jsonify({'ok': False})
            operateNum = int(data['operateNum'])
            nowTime = datetime.now()
            operateTime = nowTime.strftime('%Y-%m-%d %H:%M:%S.%f')
            documentTime = data['documentTime']
            documentNumber = datetime.now().strftime('%Y%m%d%H%M%S%f')  # 使用时间戳生成唯一代号
            documentNumber = documentNumber[0:16]  # 使用时间戳生成唯一代号
            # insert_materialInOut(documentNumber, documentTime, materialCode, isInOrOut, operateNum, unit, price, supplier, operateTime, username)
            myThread(target=insert_materialInOut, args=(documentNumber, documentTime, materialCode, isInOrOut, operateNum, unit, price, supplier, operateTime, username,))
            if isInOrOut==0:
                # update_materialInfo(materialCode, materialName, materialType, operateNum, price,unit,supplier)
                myThread(target=update_materialInfo, args=(materialCode, materialName, materialType, operateNum, price,unit,supplier,))
            elif isInOrOut==1:
                # update_materialInfo(materialCode, materialName, materialType, -operateNum, price, unit, supplier)
                myThread(target=update_materialInfo, args=(materialCode, materialName, materialType, -operateNum, price, unit, supplier,))
            return jsonify({'ok': True})
    else:
        return render_template('access_fail.html')

# xijiawei
# 物料出入库记录（显示每个物料的最近3条出入库记录）
@material_app.route('/material_inout_history', methods=['GET', 'POST'])
def material_inout_history():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        username = session['username']
        # authority = select_user_authority(username)
        thread = myThread(target=select_user_authority, args=(username,))
        authority = thread.get_result()
        if request.method == "GET":
            # materialInOut = select_all_materialInOut()
            # result = select_all_materialInOut()
            thread = myThread(target=select_all_materialInOut,args=())
            result = thread.get_result()
            materialInOut=[]
            for i in result:
                materialInOut.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12][0:21],i[13]])
            # materialInOutSums = select_sum_materialInOut()
            thread = myThread(target=select_sum_materialInOut, args=())
            materialInOutSums = thread.get_result()
            mSumTitle=""
            mSumNum=""
            mSumAmount=""
            for i in materialInOutSums:
                if i[0]==0:
                    mSumTitle+="入库/"
                    mSumNum = mSumNum + str(i[1]) + "/"
                    mSumAmount = mSumAmount + str(i[2]) + "/"
                if i[0]==1:
                    mSumTitle+="出库"
                    mSumNum = mSumNum + str(i[1])
                    mSumAmount = mSumAmount + str(i[2])
            nowTime = datetime.now().strftime('%Y-%m-%d')
            return render_template('material_inout_history.html', authority=authority[0], materialInOut=materialInOut, materialInOutCount=[mSumTitle,mSumNum,mSumAmount], username=username,nowTime=nowTime)
        if request.method == "POST":
            data = request.get_json()
            materialCode = data['materialCode']
            isInOrOut = data['isInOrOut']
            operateNum = data['operateNum']
            unit = data['unit']
            price = data['price']
            supplier = data['supplier']
            documentNumber = data['documentNumber']
            documentTime=data['documentTime']
            operateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            # materialInfo=select_materialInfoByCode(materialCode)
            thread = myThread(target=select_materialInfoByCode, args=(materialCode,))
            materialInfo = thread.get_result()
            beforeInventoryNum=0
            if materialInfo:
                beforeInventoryNum=materialInfo[0][3]
            # update_materialInOut(documentNumber, documentTime, isInOrOut, operateNum, unit, price, supplier, operateTime, username, beforeInventoryNum)
            myThread(target=update_materialInOut,args=(documentNumber, documentTime, isInOrOut, operateNum, unit, price, supplier, operateTime, username, beforeInventoryNum,))
            return jsonify({'ok': True,'beforeInventoryNum':beforeInventoryNum,'operateTime':operateTime[0:19],'operatorName':username})
    else:
        return render_template('access_fail.html')

# xijiawei
# 查询物料出入库记录（根据时间段）
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
            # materials=select_all_materialInOutFilterByDate(startDate, endDate)
            # result = select_all_materialInOutFilterByDate(startDate, endDate)
            thread = myThread(target=select_all_materialInOutFilterByDate, args=(startDate, endDate,))
            result = thread.get_result()
            materials=[]
            for i in result:
                materials.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12][0:21],i[13]])
            return jsonify({'materials': materials})
    else:
        return jsonify({'ok': False})

# xijiawei
# 删除物料出入库记录
@material_app.route('/delete_material_inout', methods=['POST'])
def delete_material_inout():
    print(session)
    print(session.keys())
    print(session.get('username'))
    if session.get('username'):
        if request.method == "POST":
            data = request.get_json()
            documentNumber = data['documentNumber']
            # delete_materialInOutByDocNum(documentNumber)
            myThread(target=delete_materialInOutByDocNum, args=(documentNumber,))
            return jsonify({'ok': True})
    else:
        return jsonify({'ok': False})
