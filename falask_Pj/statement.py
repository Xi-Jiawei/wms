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

            thread = myThread(target=select_addReceivableSumByMonth, args=(month,))
            revenue = thread.get_result()
            thread = myThread(target=select_addPayableSumByMonth, args=(month,))
            materialExpense = thread.get_result()
            thread = myThread(target=select_workerSalarySumByMonth, args=(month,))
            workerSalaryExpense = thread.get_result()[0][15]
            thread = myThread(target=select_managerSalarySumByMonth, args=(month,))
            managerSalaryExpense = thread.get_result()[0][17]
            thread = myThread(target=select_supplementaryAddPayableSumByMonth, args=(month,))
            supplementaryExpense = thread.get_result()
            thread = myThread(target=select_operationSumByMonth, args=(month,))
            operationExpense = thread.get_result()
            thread = myThread(target=select_aftersaleSumByMonth, args=(month,))
            aftersaleExpense = thread.get_result()[0]+thread.get_result()[1]+thread.get_result()[2]

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
            thread = myThread(target=select_addReceivableSumByMonth, args=(month,))
            revenue = thread.get_result()
            thread = myThread(target=select_addPayableSumByMonth, args=(month,))
            materialExpense = thread.get_result()
            thread = myThread(target=select_workerSalarySumByMonth, args=(month,))
            workerSalaryExpense = thread.get_result()[0][15]
            thread = myThread(target=select_managerSalarySumByMonth, args=(month,))
            managerSalaryExpense = thread.get_result()[0][17]
            thread = myThread(target=select_supplementaryAddPayableSumByMonth, args=(month,))
            supplementaryExpense = thread.get_result()
            thread = myThread(target=select_operationSumByMonth, args=(month,))
            operationExpense = thread.get_result()
            thread = myThread(target=select_aftersaleSumByMonth, args=(month,))
            aftersaleExpense = thread.get_result()[0]+thread.get_result()[1]+thread.get_result()[2]

            # 损益
            income=revenue-materialExpense-workerSalaryExpense-managerSalaryExpense-supplementaryExpense-operationExpense-aftersaleExpense
            salaryExpense = workerSalaryExpense + managerSalaryExpense
            otherExpense = supplementaryExpense + operationExpense + aftersaleExpense
            return render_template('statement.html', form=form, username=username, income=income, revenue=revenue, materialExpense=materialExpense, salaryExpense=salaryExpense, otherExpense=otherExpense, month=month)
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
                thread = myThread(target=select_all_clients, args=())
                clients = thread.get_result()
                remainReceivableSum = 0
                addReceivableSum = 0
                receivableSum = 0
                receiptSum = 0
                for client in clients:
                    thread = myThread(target=select_receivableReportByCode, args=(client[0], month,))
                    receivable = thread.get_result()
                    remainReceivableSum += receivable[0][1]
                    addReceivableSum += receivable[0][2]
                    receivableSum += receivable[0][3]
                    receiptSum += receivable[0][4]
                receivable = [remainReceivableSum, addReceivableSum, receivableSum, receiptSum]
                thread = myThread(target=select_all_receivableReportGroupByProductType, args=(month,))  # productType, addDeliveryNum, price, addReceivable, receivable, remark
                receivablesOfProduct = thread.get_result()
            else:
                thread = myThread(target=select_receivableReportByCode, args=(clientCode, month,))
                receivable = thread.get_result()
                thread = myThread(target=select_receivableReportGroupByProductTypeByCode, args=(
                clientCode, month,))  # productType, addDeliveryNum, price, addReceivable, receivable, remark
                receivablesOfProduct = thread.get_result()
            return jsonify({'ok': True,'receivable':receivable,'receivablesOfProduct':receivablesOfProduct})
        elif request.method=="GET":
            form = ProductForm()
            month = datetime.now().strftime('%Y-%m')
            thread = myThread(target=select_all_clients, args=())
            clients = thread.get_result()
            remainReceivableSum = 0
            addReceivableSum = 0
            receivableSum = 0
            receiptSum = 0
            for client in clients:
                thread = myThread(target=select_receivableReportByCode, args=(client[0], month,))
                receivable = thread.get_result()
                remainReceivableSum += receivable[0][1]
                addReceivableSum += receivable[0][2]
                receivableSum += receivable[0][3]
                receiptSum += receivable[0][4]
            receivable=[remainReceivableSum,addReceivableSum,receivableSum,receiptSum]
            thread = myThread(target=select_all_receivableReportGroupByProductType, args=(month,)) # productType, addDeliveryNum, price, addReceivable, receivable, remark
            receivablesOfProduct = thread.get_result()
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
                thread = myThread(target=select_all_suppliers, args=())
                suppliers = thread.get_result()
                remainPayableSum = 0
                addPayableSum = 0
                payableSum = 0
                paymentSum = 0
                for supplier in suppliers:
                    thread = myThread(target=select_payableReportByCode, args=(supplier[0], month,))
                    payable = thread.get_result()
                    remainPayableSum += payable[0][1]
                    addPayableSum += payable[0][2]
                    payableSum += payable[0][3]
                    paymentSum += payable[0][4]
                payable = [remainPayableSum, addPayableSum, payableSum, paymentSum]
                thread = myThread(target=select_all_payableReportGroupByMaterialCode, args=(month,))  # productType, addDeliveryNum, price, addReceivable, receivable, remark
                payablesOfMaterial = thread.get_result()
            else:
                thread = myThread(target=select_payableReportByCode, args=(supplierCode, month,))
                payable = thread.get_result()
                thread = myThread(target=select_payableReportGroupByMaterialCodeByCode, args=(supplierCode, month,))
                payablesOfMaterial = thread.get_result()
            return jsonify({'ok': True,'payable':payable,'payablesOfMaterial':payablesOfMaterial})
        elif request.method=="GET":
            username = session['username']
            form = ProductForm()
            month = datetime.now().strftime('%Y-%m')
            thread = myThread(target=select_all_suppliers, args=())
            suppliers = thread.get_result()
            remainPayableSum = 0
            addPayableSum = 0
            payableSum = 0
            paymentSum = 0
            for supplier in suppliers:
                thread = myThread(target=select_payableReportByCode, args=(supplier[0], month,))
                payable = thread.get_result()
                remainPayableSum += payable[0][1]
                addPayableSum += payable[0][2]
                payableSum += payable[0][3]
                paymentSum += payable[0][4]
            payable=[remainPayableSum,addPayableSum,payableSum,paymentSum]
            thread = myThread(target=select_all_payableReportGroupByMaterialCode, args=(month,)) # productType, addDeliveryNum, price, addReceivable, receivable, remark
            payablesOfMaterial = thread.get_result()
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
            form = ProductForm()
            month=datetime.now().strftime('%Y-%m')
            thread = myThread(target=select_workerSalaryByMonth, args=(month, ))
            workerSalary = thread.get_result()
            thread = myThread(target=select_managerSalaryByMonth, args=(month, ))
            managerSalary = thread.get_result()

            thread = myThread(target=select_workerSalarySumByMonth, args=(month,))
            workerSalarySum = thread.get_result()
            thread = myThread(target=select_managerSalarySumByMonth, args=(month,))
            managerSalarySum = thread.get_result()
            return render_template('statement_salary.html', form=form, username=username, workerSalary=workerSalary, managerSalary=managerSalary, workerSalarySum=workerSalarySum, managerSalarySum=managerSalarySum, month=month)
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@statement_app.route('/search_worker_salary/<month>', methods=['GET'])
def search_worker_salary(month):
    if session.get('username'):
        if request.method == "GET":
            thread = myThread(target=select_workerSalaryByMonth,args=(month,))
            salaries = thread.get_result()
            thread = myThread(target=select_workerSalarySumByMonth,args=(month,))
            # salarySum = thread.get_result()
            result = thread.get_result()[0]
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
            thread = myThread(target=select_managerSalaryByMonth,args=(month,))
            salaries = thread.get_result()
            thread = myThread(target=select_managerSalarySumByMonth,args=(month,))
            # salarySum = thread.get_result()
            result = thread.get_result()[0]
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
            thread = myThread(target=select_all_supplementarySuppliers, args=())
            suppliers = thread.get_result()
            remainPayableSum = 0
            addPayableSum = 0
            payableSum = 0
            paymentSum = 0
            for i in suppliers:
                thread = myThread(target=select_supplementaryPayableReportByCode, args=(i[0], month,))
                payable = thread.get_result()
                remainPayableSum += payable[0][1]
                addPayableSum += payable[0][2]
                payableSum += payable[0][3]
                paymentSum += payable[0][4]
            supplementaryPayableSum=[remainPayableSum,addPayableSum,payableSum,paymentSum]
            thread = myThread(target=select_all_supplementary, args=(month,))
            supplementaryPayables = thread.get_result()

            thread = myThread(target=select_operationSelect, args=())
            operationSelects = thread.get_result()
            thread = myThread(target=select_operationsByMonth, args=(month,))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operations = thread.get_result()
            thread = myThread(target=select_operationSumByMonth, args=(month,))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = thread.get_result()

            thread = myThread(target=select_aftersalesByMonth, args=(month,))  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersales = thread.get_result()
            thread = myThread(target=select_aftersaleSumByMonth, args=(month,))  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleSum = thread.get_result()
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
                thread = myThread(target=select_all_supplementarySuppliers, args=())
                suppliers = thread.get_result()
                remainPayableSum = 0
                addPayableSum = 0
                payableSum = 0
                paymentSum = 0
                for i in suppliers:
                    thread = myThread(target=select_supplementaryPayableReportByCode, args=(i[0], month,))
                    payable = thread.get_result()
                    remainPayableSum += payable[0][1]
                    addPayableSum += payable[0][2]
                    payableSum += payable[0][3]
                    paymentSum += payable[0][4]
                payable = [remainPayableSum, addPayableSum, payableSum, paymentSum]
                thread = myThread(target=select_all_supplementary, args=(month,))
                supplementaryArr = thread.get_result()
            else:
                thread = myThread(target=select_supplementaryPayableReportByCode, args=(supplierCode, month,))
                payable = thread.get_result()
                thread = myThread(target=select_supplementaryByCodeAndMonth, args=(supplierCode, month,))
                supplementaryArr = thread.get_result()
            return jsonify({'ok': True,'payable':payable,'supplementaryArr':supplementaryArr})
    else:
        return render_template('access_fail.html')
