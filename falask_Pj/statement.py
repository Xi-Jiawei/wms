from flask import render_template, request, session, Blueprint, jsonify

from db import *
from form import *

from datetime import datetime

statement_app=Blueprint('statement',__name__)

# xijiawei
# 订单管理
@statement_app.route('/statement', methods=['GET'])
def statement():
    if session.get('username'):
        if request.method == "POST":
            print("")
        elif request.method=="GET":
            username = session['username']
            form = ProductForm()
            return render_template('statement.html', form=form, username=username)
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@statement_app.route('/statement_receivable', methods=['GET','POST'])
def statement_receivable():
    if session.get('username'):
        if request.method == "POST":
            data = request.get_json()
            clientCode = data['clientCode']
            month = data['month']
            thread = myThread(target=select_receivableReportByCode, args=(clientCode, month,))
            receivable = thread.get_result()
            thread = myThread(target=select_receivableReportGroupByProductTypeByCode, args=(clientCode, month,)) # productType, addDeliveryNum, price, addReceivable, receivable, remark
            receivablesOfProduct = thread.get_result()
            return jsonify({'ok': True,'receivable':receivable,'receivablesOfProduct':receivablesOfProduct})
        elif request.method=="GET":
            username = session['username']
            form = ProductForm()
            month = datetime.now().strftime('%Y-%m')
            return render_template('statement_receivable_detail.html', form=form, username=username, month=month)
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
            thread = myThread(target=select_payableReportByCode, args=(supplierCode, month,))
            payable = thread.get_result()
            thread = myThread(target=select_payableReportGroupByMaterialCodeByCode, args=(supplierCode, month,))
            payablesOfMaterial = thread.get_result()
            return jsonify({'ok': True,'payable':payable,'payablesOfMaterial':payablesOfMaterial})
        elif request.method=="GET":
            username = session['username']
            form = ProductForm()
            month = datetime.now().strftime('%Y-%m')
            return render_template('statement_payable.html', form=form, username=username, month=month)
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
            salarySum = thread.get_result()
            return jsonify({'ok': True,'salaries':salaries,'salarySum':salarySum})
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
            salarySum = thread.get_result()
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
            thread = myThread(target=select_operationsByMonth, args=(month,))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operations = thread.get_result()
            thread = myThread(target=select_operationSumByMonth, args=(month,))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = thread.get_result()

            thread = myThread(target=select_aftersalesByMonth, args=(month,))  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersales = thread.get_result()
            thread = myThread(target=select_aftersaleSumByMonth, args=(month,))  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleSum = thread.get_result()
            return render_template('statement_othercosts.html', form=form, username=username, operations=operations, operationSum=operationSum, aftersales=aftersales, aftersaleSum=aftersaleSum, month=month)
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
            thread = myThread(target=select_supplementaryPayableReportByCode, args=(supplierCode, month,))
            payable = thread.get_result()
            thread = myThread(target=select_supplementaryByCodeAndMonth, args=(supplierCode, month,))
            supplementaryArr = thread.get_result()
            return jsonify({'ok': True,'payable':payable,'supplementaryArr':supplementaryArr})
    else:
        return render_template('access_fail.html')
