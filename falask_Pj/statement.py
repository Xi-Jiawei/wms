from flask import render_template, request, session, Blueprint, jsonify

from db import *
from form import *

from datetime import datetime

statement_app=Blueprint('statement',__name__)

# xijiawei
# 订单管理
@statement_app.route('/statement', methods=['GET','POST'])
def statement():
    if session.get('username'):
        if request.method == "POST":
            data = request.get_json()
            month = data['month']

            revenue = select_addReceivableSumByMonth(month)
            materialExpense = select_addPayableSumByMonth(month)
            workerSalaryExpense = select_workerSalarySumByMonth(month)[0][15]
            managerSalaryExpense = select_managerSalarySumByMonth(month)[0][17]
            supplementaryExpense = select_supplementaryAddPayableSumByMonth(month)
            operationExpense = select_operationSumByMonth(month)
            aftersaleSum = select_aftersaleSumByMonth(month)  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleExpense = aftersaleSum[0] + aftersaleSum[1] + aftersaleSum[2]

            # 损益
            income = revenue - materialExpense - workerSalaryExpense - managerSalaryExpense - supplementaryExpense - operationExpense - aftersaleExpense
            salaryExpense = workerSalaryExpense + managerSalaryExpense
            otherExpense = supplementaryExpense + operationExpense + aftersaleExpense

            incomeDetail=[month,revenue,materialExpense,salaryExpense,otherExpense,income]
            return jsonify({'ok': True,'incomeDetail':incomeDetail})
        elif request.method=="GET":
            username = session['username']
            form = ProductForm()

            month = datetime.now().strftime('%Y-%m')
            revenue = select_addReceivableSumByMonth(month)
            materialExpense = select_addPayableSumByMonth(month)
            workerSalaryExpense = select_workerSalarySumByMonth(month)[0][15]
            managerSalaryExpense = select_managerSalarySumByMonth(month)[0][17]
            supplementaryExpense = select_supplementaryAddPayableSumByMonth(month)
            operationExpense = select_operationSumByMonth(month)
            aftersaleSum = select_aftersaleSumByMonth(month)  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleExpense = aftersaleSum[0] + aftersaleSum[1] + aftersaleSum[2]

            # 损益
            income=revenue-materialExpense-workerSalaryExpense-managerSalaryExpense-supplementaryExpense-operationExpense-aftersaleExpense
            salaryExpense = workerSalaryExpense + managerSalaryExpense
            otherExpense = supplementaryExpense + operationExpense + aftersaleExpense
            return render_template('statement.html', form=form, username=username, income=round(income,2), revenue=round(revenue,2), materialExpense=round(materialExpense,2), salaryExpense=round(salaryExpense,2), otherExpense=round(otherExpense,2), month=month)
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@statement_app.route('/statement_receivable', methods=['GET','POST'])
def statement_receivable():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            clientCode = data['clientCode']
            month = data['month']
            if clientCode=="":
                clients = select_all_clients()
                remainReceivableSum = 0
                addReceivableSum = 0
                receivableSum = 0
                receiptSum = 0
                for client in clients:
                    receivable = select_receivableReportByCode(client[0], month)
                    remainReceivableSum += receivable[0][1]
                    addReceivableSum += receivable[0][2]
                    receivableSum += receivable[0][3]
                    receiptSum += receivable[0][4]
                receivable=[round(remainReceivableSum,2),round(addReceivableSum,2),round(receivableSum,2),round(receiptSum,2)]
                receivablesOfProduct = select_all_receivableReportGroupByProductType(month) # productType, addDeliveryNum, price, addReceivable, receivable, remark
                return jsonify({'ok': True, 'receivable': receivable, 'receivablesOfProduct': receivablesOfProduct})
            else:
                clientInfo = select_clientByCode(clientCode)
                if clientInfo:
                    result = select_receivableReportByCode(clientCode, month)
                    receivable = [result[0][1], result[0][2], result[0][3], result[0][4]]
                    receivablesOfProduct = select_receivableReportGroupByProductTypeByCode(clientCode,month) # productType, addDeliveryNum, price, addReceivable, receivable, remark
                    return jsonify({'ok': True, 'receivable': receivable, 'receivablesOfProduct': receivablesOfProduct})
                else:
                    receivable = [0, 0, 0, 0]
                    receivablesOfProduct = []
                    return jsonify({'ok': False, 'receivable': receivable, 'receivablesOfProduct': receivablesOfProduct})
        elif request.method=="GET":
            form = ProductForm()
            month = datetime.now().strftime('%Y-%m')
            clients = select_all_clients()
            remainReceivableSum = 0
            addReceivableSum = 0
            receivableSum = 0
            receiptSum = 0
            for client in clients:
                receivable = select_receivableReportByCode(client[0], month)
                remainReceivableSum += receivable[0][1]
                addReceivableSum += receivable[0][2]
                receivableSum += receivable[0][3]
                receiptSum += receivable[0][4]
            receivable=[round(remainReceivableSum,2),round(addReceivableSum,2),round(receivableSum,2),round(receiptSum,2),round(receivableSum-receiptSum,2)]
            receivablesOfProduct = select_all_receivableReportGroupByProductType(month) # productType, addDeliveryNum, price, addReceivable, receivable, remark
            return render_template('statement_receivable_detail.html', form=form, username=username, month=month, receivablesOfProduct=receivablesOfProduct, receivable=receivable)
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@statement_app.route('/statement_payable', methods=['GET','POST'])
def statement_payable():
    if session.get('username'):
        if request.method == "POST":
            data = request.get_json()
            supplierCode = data['supplierCode']
            month = data['month']
            if supplierCode=="":
                suppliers = select_all_suppliers()
                remainPayableSum = 0
                addPayableSum = 0
                payableSum = 0
                paymentSum = 0
                for supplier in suppliers:
                    payable = select_payableReportByCode(supplier[0], month)
                    remainPayableSum += payable[0][1]
                    addPayableSum += payable[0][2]
                    payableSum += payable[0][3]
                    paymentSum += payable[0][4]
                payable = [round(remainPayableSum,2), round(addPayableSum,2), round(payableSum,2), round(paymentSum,2)]
                payablesOfMaterial = select_all_payableReportGroupByMaterialCode(month) # productType, addDeliveryNum, price, addReceivable, receivable, remark
                return jsonify({'ok': True, 'payable': payable, 'payablesOfMaterial': payablesOfMaterial})
            else:
                supplierInfo = select_supplierByCode(supplierCode)
                if supplierInfo:
                    result = select_payableReportByCode(supplierCode, month)
                    payable = [result[0][1], result[0][2], result[0][3], result[0][4]]
                    payablesOfMaterial = select_payableReportGroupByMaterialCodeByCode(supplierCode, month)
                    return jsonify({'ok': True, 'payable': payable, 'payablesOfMaterial': payablesOfMaterial})
                else:
                    payable = [0, 0, 0, 0]
                    payablesOfMaterial = []
                    return jsonify({'ok': False, 'payable': payable, 'payablesOfMaterial': payablesOfMaterial})
        elif request.method=="GET":
            username = session['username']
            form = ProductForm()
            month = datetime.now().strftime('%Y-%m')
            suppliers = select_all_suppliers()
            remainPayableSum = 0
            addPayableSum = 0
            payableSum = 0
            paymentSum = 0
            for supplier in suppliers:
                payable = select_payableReportByCode(supplier[0], month)
                remainPayableSum += payable[0][1]
                addPayableSum += payable[0][2]
                payableSum += payable[0][3]
                paymentSum += payable[0][4]
            payable = [round(remainPayableSum,2), round(addPayableSum,2), round(payableSum,2), round(paymentSum,2), round(payableSum-paymentSum,2)]
            payablesOfMaterial = select_all_payableReportGroupByMaterialCode(month) # productType, addDeliveryNum, price, addReceivable, receivable, remark
            return render_template('statement_payable.html', form=form, username=username, month=month, payablesOfMaterial=payablesOfMaterial, payable=payable)
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@statement_app.route('/statement_salary', methods=['GET'])
def statement_salary():
    if session.get('username'):
        if request.method=="GET":
            username = session['username']
            authority = select_user_authority(username)
            form = ProductForm()
            month=datetime.now().strftime('%Y-%m')
            workerSalary = select_workerSalaryByMonth(month)
            managerSalary = select_managerSalaryByMonth(month)

            workerSalarySum = select_workerSalarySumByMonth(month)
            managerSalarySum = select_managerSalarySumByMonth(month)
            return render_template('statement_salary.html', form=form, username=username, authority=authority[1], workerSalary=workerSalary, managerSalary=managerSalary, workerSalarySum=workerSalarySum, managerSalarySum=managerSalarySum, month=month)
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@statement_app.route('/search_worker_salary/<month>', methods=['GET'])
def search_worker_salary(month):
    if session.get('username'):
        if request.method == "GET":
            salaries = select_workerSalaryByMonth(month)
            result = select_workerSalarySumByMonth(month)[0]
            salarySum = []
            salarySum.append(result[0])
            if result[1]:
                for i in range(len(result) - 1):
                    salarySum.append(float(result[i + 1]))
            else:
                for i in range(len(result) - 1):
                    salarySum.append(0)
            return jsonify({'ok': True,'salaries':salaries, 'salarySum':salarySum})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@statement_app.route('/search_manager_salary/<month>', methods=['GET'])
def search_manager_salary(month):
    if session.get('username'):
        if request.method == "GET":
            salaries = select_managerSalaryByMonth(month)
            result = select_managerSalarySumByMonth(month)[0]
            salarySum = []
            salarySum.append(result[0])
            if result[1]:
                for i in range(len(result) - 1):
                    salarySum.append(float(result[i + 1]))
            else:
                for i in range(len(result) - 1):
                    salarySum.append(0)
            return jsonify({'ok': True,'salaries':salaries,'salarySum':salarySum})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@statement_app.route('/statement_othercosts', methods=['GET'])
def statement_othercosts():
    if session.get('username'):
        if request.method=="GET":
            username = session['username']
            form = ProductForm()

            month = datetime.now().strftime('%Y-%m')
            suppliers = select_all_supplementarySuppliers()
            remainPayableSum = 0
            addPayableSum = 0
            payableSum = 0
            paymentSum = 0
            for i in suppliers:
                payable = select_supplementaryPayableReportByCode(i[0], month) # supplierCode,remainPayable,addPayable,payable,payment,remark
                remainPayableSum += payable[0][1]
                addPayableSum += payable[0][2]
                payableSum += payable[0][3]
                paymentSum += payable[0][4]
            supplementaryPayableSum=[round(remainPayableSum,2),round(addPayableSum,2),round(payableSum,2),round(paymentSum,2)]
            supplementaryPayables = select_all_supplementary(month)

            operationSelects = select_operationSelect()
            operations = select_operationsByMonth(month) # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = select_operationSumByMonth(month)

            aftersales = select_aftersalesByMonth(month) # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleSum = select_aftersaleSumByMonth(month)  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            return render_template('statement_othercosts.html', form=form, username=username, supplementaryPayableSum=supplementaryPayableSum, supplementaryPayables=supplementaryPayables, operationSelects=operationSelects, operations=operations, operationSum=operationSum, aftersales=aftersales, aftersaleSum=aftersaleSum, month=month)
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@statement_app.route('/statement_supplementary_payable', methods=['POST'])
def statement_supplementary_payable():
    if session.get('username'):
        if request.method == "POST":
            data = request.get_json()
            supplierCode = data['supplierCode']
            month = data['month']
            if supplierCode=="":
                suppliers = select_all_supplementarySuppliers()
                remainPayableSum = 0
                addPayableSum = 0
                payableSum = 0
                paymentSum = 0
                for i in suppliers:
                    payable = select_supplementaryPayableReportByCode(i[0], month) # supplierCode,remainPayable,addPayable,payable,payment,remark
                    remainPayableSum += payable[0][1]
                    addPayableSum += payable[0][2]
                    payableSum += payable[0][3]
                    paymentSum += payable[0][4]
                payable = [round(remainPayableSum,2),round(addPayableSum,2),round(payableSum,2),round(paymentSum,2)]
                supplementaryArr = select_all_supplementary(month)
            else:
                payable = select_supplementaryPayableReportByCode(supplierCode, month) # supplierCode,remainPayable,addPayable,payable,payment,remark
                supplementaryArr = select_supplementaryByCodeAndMonth(supplierCode, month)
            return jsonify({'ok': True,'payable':payable,'supplementaryArr':supplementaryArr})
    else:
        return render_template('access_fail.html')
