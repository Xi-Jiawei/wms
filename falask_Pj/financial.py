from flask import render_template, request, session, Blueprint, jsonify

from db import *
from form import *

from datetime import datetime

financial_app=Blueprint('financial',__name__)

##### 收款记账 #####

# xijiawei
# 订单管理
@financial_app.route('/financial_receivable', methods=['GET'])
def financial_receivable():
    if session.get('username'):
        if request.method=="GET":
            username = session['username']
            form = ProductForm()

            month = datetime.now().strftime('%Y-%m')
            thread = myThread(target=select_all_clients, args=())
            clients = thread.get_result()
            receivables = []
            remainReceivableSum = 0
            addReceivableSum = 0
            receivableSum = 0
            receiptSum = 0
            for i in clients:
                receivable = []
                thread = myThread(target=select_receivableReportByCode, args=(i[0], month,))
                result = thread.get_result()
                receivable.append(result[0][0])
                receivable.append(i[1]) # historyReceivable
                receivable.append(result[0][1])
                receivable.append(result[0][2])
                receivable.append(result[0][3])
                receivable.append(result[0][4])
                receivable.append(result[0][5])
                receivables.append(receivable)

                remainReceivableSum += result[0][1]
                addReceivableSum += result[0][2]
                receivableSum += result[0][3]
                receiptSum += result[0][4]
            sum = [round(remainReceivableSum,2), round(addReceivableSum,2), round(receivableSum,2), round(receiptSum,2)]
            return render_template('financial_receivable.html', form=form, receivables=receivables, sum=sum, username=username)
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/financial_receipts/<clientCode>', methods=['GET','POST'])
def financial_receipts(clientCode):
    if session.get('username'):
        username = session['username']
        if request.method=="POST":
            data = request.get_json()
            clientCode = data['clientCode']  # 不要写成orderCode=request.data["orderCode"]
            beforeReceivable = float(data['beforeReceivable'])
            receiptDate = data['receiptDate']
            receipt = float(data['receipt'])
            remark = data['remark']
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            myThread(target=insert_receiptsJournal, args=(clientCode,receiptDate,beforeReceivable,receipt,remark,entryTime,entryClerk,))
            return jsonify({'ok': True})
        elif request.method=="GET":
            thread = myThread(target=select_receiptsJournal, args=(clientCode,))
            receipts = thread.get_result()
            return jsonify({'ok': True,'receipts':receipts})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/financial_history_receivable', methods=['GET','POST'])
def financial_history_receivable():
    if session.get('username'):
        username = session['username']
        if request.method=="POST":
            data = request.get_json()
            clientCode = data['clientCode']  # 不要写成orderCode=request.data["orderCode"]
            historyReceivable = float(data['historyReceivable'])
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            myThread(target=update_historyReceivable, args=(clientCode,historyReceivable,entryTime,entryClerk,))
            return jsonify({'ok': True})
    else:
        return render_template('access_fail.html')

##### 付款记账 #####

# xijiawei
# 订单管理
@financial_app.route('/financial_payable', methods=['GET'])
def financial_payable():
    if session.get('username'):
        if request.method=="GET":
            username = session['username']
            form = ProductForm()

            month = datetime.now().strftime('%Y-%m')
            thread = myThread(target=select_all_suppliers, args=())
            suppliers = thread.get_result()
            payables = []
            remainPayableSum = 0
            addPayableSum = 0
            payableSum = 0
            paymentSum = 0
            for i in suppliers:
                payable = []
                thread = myThread(target=select_payableReportByCode, args=(i[0], month,))
                result = thread.get_result()
                payable.append(result[0][0])
                payable.append(i[1]) # historyPayable
                payable.append(result[0][1])
                payable.append(result[0][2])
                payable.append(result[0][3])
                payable.append(result[0][4])
                payable.append(result[0][5])
                payables.append(payable)

                remainPayableSum += result[0][1]
                addPayableSum += result[0][2]
                payableSum += result[0][3]
                paymentSum += result[0][4]
            sum = [round(remainPayableSum,2), round(addPayableSum,2), round(payableSum,2), round(paymentSum,2)]
            return render_template('financial_payable.html', form=form, username=username, sum=sum, payables=payables)
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/financial_payments/<supplierCode>', methods=['GET','POST'])
def financial_payments(supplierCode):
    if session.get('username'):
        username = session['username']
        if request.method=="POST":
            data = request.get_json()
            supplierCode = data['supplierCode']  # 不要写成orderCode=request.data["orderCode"]
            beforePayable = float(data['beforePayable'])
            paymentDate = data['paymentDate']
            payment = float(data['payment'])
            remark = data['remark']
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            myThread(target=insert_paymentsJournal, args=(supplierCode,paymentDate,beforePayable,payment,remark,entryTime,entryClerk,))
            return jsonify({'ok': True})
        elif request.method=="GET":
            thread = myThread(target=select_paymentsJournal, args=(supplierCode,))
            payments = thread.get_result()
            return jsonify({'ok': True,'payments':payments})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/search_supplier/<filterStr>', methods=['GET'])
def search_supplier(filterStr):
    if session.get('username'):
        username = session['username']
        if request.method == "GET":
            thread = myThread(target=select_supplierInfoByFilter, args=(filterStr,))  # client, address, contact, telephone
            suppliers = thread.get_result()
            return jsonify({'ok': True,'suppliers':suppliers})
    else:
        return jsonify({'ok': False})

# xijiawei
# 订单管理
@financial_app.route('/financial_history_payable', methods=['GET','POST'])
def financial_history_payable():
    if session.get('username'):
        username = session['username']
        if request.method=="POST":
            data = request.get_json()
            supplierCode = data['supplierCode']  # 不要写成orderCode=request.data["orderCode"]
            historyPayable = float(data['historyPayable'])
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            myThread(target=update_historyPayable, args=(supplierCode,historyPayable,entryTime,entryClerk,))
            return jsonify({'ok': True})
    else:
        return render_template('access_fail.html')

##### 工资管理 #####

# xijiawei
# 订单管理
@financial_app.route('/financial_salary', methods=['GET'])
def financial_salary():
    if session.get('username'):
        if request.method == "POST":
            print("")
        elif request.method=="GET":
            username = session['username']
            form = ProductForm()

            month=datetime.now().strftime('%Y-%m')
            thread = myThread(target=select_all_workerSalary, args=())
            workerSalary = thread.get_result()
            thread = myThread(target=select_all_managerSalary, args=())
            managerSalary = thread.get_result()
            thread = myThread(target=select_workerSalarySumByMonth, args=(month,))
            workerSalarySum = thread.get_result()
            thread = myThread(target=select_managerSalarySumByMonth, args=(month,))
            managerSalarySum = thread.get_result()
            return render_template('financial_salary.html', form=form, username=username, workerSalary=workerSalary, managerSalary=managerSalary, workerSalarySum=workerSalarySum, managerSalarySum=managerSalarySum, month=month)
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/add_worker_salary', methods=['POST'])
def add_worker_salary():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            name = data['name']
            position = data['position']
            workhours = data['workhours']
            overhours = data['overhours']
            timewage = data['timewage']
            piecewage = data['piecewage']
            workagewage = data['workagewage']
            subsidy = data['subsidy']
            amerce = data['amerce']
            tax = data['tax']
            socialSecurityOfPersonal = data['socialSecurityOfPersonal']
            otherdues = 0
            socialSecurityOfEnterprise = data['socialSecurityOfEnterprise']
            payablewage = timewage+piecewage+workagewage+subsidy-amerce
            aftertaxwage = payablewage-tax
            realwage = aftertaxwage-socialSecurityOfPersonal-otherdues
            salaryExpense = payablewage+socialSecurityOfEnterprise
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            thread=myThread(target=insert_workerSalary, args=(entryTime[0:7], name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk,))
            staffid = thread.get_result()
            return jsonify({'ok': True, 'month': entryTime[0:7], 'staffid': staffid})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/edit_worker_salary', methods=['POST'])
def edit_worker_salary():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            salaries = data['salaries']
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            for i in salaries:
                month = i[0]
                staffid = i[1]
                name = i[2]
                position = i[3]
                workhours = i[4]
                overhours = i[5]
                timewage = i[6]
                piecewage = i[7]
                workagewage = i[8]
                subsidy = i[9]
                amerce = i[10]
                tax = i[11]
                socialSecurityOfPersonal = i[12]
                otherdues = i[13]
                socialSecurityOfEnterprise = i[14]
                payablewage = timewage + piecewage + workagewage + subsidy - amerce
                aftertaxwage = payablewage - tax
                realwage = aftertaxwage - socialSecurityOfPersonal - otherdues
                salaryExpense = payablewage + socialSecurityOfEnterprise
                if staffid=="":
                    myThread(target=insert_workerSalary, args=(month, name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk,))
                else:
                    myThread(target=update_workerSalary,args=(month, int(staffid), name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk,))

            month=datetime.now().strftime('%Y-%m')
            thread = myThread(target=select_all_workerSalary, args=())
            salaryArr = thread.get_result()
            thread = myThread(target=select_workerSalarySumByMonth, args=(month,))
            # workerSalarySum = thread.get_result()
            result = thread.get_result()[0]
            workerSalarySum = []
            workerSalarySum.append(result[0])
            if result[1]:
                for i in range(len(result) - 1):
                    workerSalarySum.append(float(result[i + 1]))
            else:
                for i in range(len(result) - 1):
                    workerSalarySum.append(0)
            return jsonify({'ok': True, 'salaryArr': salaryArr, 'workerSalarySum': workerSalarySum})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/delete_workerSalaries', methods=['POST'])
def delete_workerSalaries():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            staffidArr = data['staffidArr']
            for i in staffidArr:
                # myThread(target=delete_staffByID,args=(int(i), ))
                myThread(target=delete_workerSalaryByIDAndMonth,args=(int(i[1]), i[0] ))
            return jsonify({'ok': True})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/add_manager_salary', methods=['POST'])
def add_manager_salary():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            name = data['name']
            position = data['position']
            workhours = data['workhours']
            overhours = data['overhours']
            basewage = data['basewage']
            jobwage = data['jobwage']
            overtimewage = data['overtimewage']
            performancewage = data['performancewage']
            workagewage = data['workagewage']
            subsidy = data['subsidy']
            amerce = data['amerce']
            tax = data['tax']
            socialSecurityOfPersonal = data['socialSecurityOfPersonal']
            otherdues = 0
            socialSecurityOfEnterprise = data['socialSecurityOfEnterprise']
            payablewage = basewage+jobwage+overtimewage+performancewage+workagewage+subsidy-amerce
            aftertaxwage = payablewage-tax
            realwage = aftertaxwage-socialSecurityOfPersonal-otherdues
            salaryExpense = payablewage+socialSecurityOfEnterprise
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            thread=myThread(target=insert_managerSalary, args=(entryTime[0:7], name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk,))
            staffid = thread.get_result()
            return jsonify({'ok': True, 'month': entryTime[0:7], 'staffid': staffid})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/edit_manager_salary', methods=['POST'])
def edit_manager_salary():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            salaries = data['salaries']
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            for i in salaries:
                month = i[0]
                staffid = i[1]
                name = i[2]
                position = i[3]
                workhours = i[4]
                overhours = i[5]
                basewage = i[6]
                jobwage = i[7]
                overtimewage = i[8]
                performancewage = i[9]
                workagewage = i[10]
                subsidy = i[11]
                amerce = i[12]
                tax = i[13]
                socialSecurityOfPersonal = i[14]
                otherdues = i[15]
                socialSecurityOfEnterprise = i[16]
                payablewage = basewage + jobwage + overtimewage + performancewage + workagewage + subsidy - amerce
                aftertaxwage = payablewage - tax
                realwage = aftertaxwage - socialSecurityOfPersonal - otherdues
                salaryExpense = payablewage + socialSecurityOfEnterprise
                if staffid=="":
                    myThread(target=insert_managerSalary, args=(month, name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk,))
                else:
                    myThread(target=update_managerSalary,args=(month, int(staffid), name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk,))

            thread = myThread(target=select_all_managerSalary, args=())
            salaryArr = thread.get_result()
            thread = myThread(target=select_managerSalarySumByMonth,args=(month,))
            # managerSalarySum = thread.get_result()
            result = thread.get_result()[0]
            managerSalarySum = []
            managerSalarySum.append(result[0])
            if result[1]:
                for i in range(len(result) - 1):
                    managerSalarySum.append(float(result[i + 1]))
            else:
                for i in range(len(result) - 1):
                    managerSalarySum.append(0)
            return jsonify({'ok': True, 'salaryArr': salaryArr, 'managerSalarySum': managerSalarySum})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/delete_managerSalaries', methods=['POST'])
def delete_managerSalaries():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            staffidArr = data['staffidArr']
            for i in staffidArr:
                # myThread(target=delete_staffByID,args=(int(i), ))
                myThread(target=delete_managerSalaryByIDAndMonth,args=(int(i[1]), i[0] ))
            return jsonify({'ok': True})
    else:
        return render_template('access_fail.html')

##### 其他费用 #####

# xijiawei
# 订单管理
@financial_app.route('/financial_othercosts', methods=['GET'])
def financial_othercosts():
    if session.get('username'):
        if request.method=="GET":
            username = session['username']
            form = ProductForm()

            thread = myThread(target=select_all_supplementarySuppliers, args=())
            suppliers = thread.get_result()
            today = datetime.now().strftime('%Y-%m-%d')
            month = datetime.now().strftime('%Y-%m')
            supplementarySuppliers=[]
            remainPayableSum = 0
            addPayableSum = 0
            payableSum = 0
            paymentSum = 0
            for i in suppliers:
                thread = myThread(target=select_supplementaryPayableReportByCode, args=(i[0], month,)) # supplierCode,remainPayable,addPayable,payable,payment,remark
                payable = thread.get_result()
                supplementarySuppliers.append(payable[0])

                remainPayableSum += payable[0][1]
                addPayableSum += payable[0][2]
                payableSum += payable[0][3]
                paymentSum += payable[0][4]
            supplementaryPayableSum = [round(remainPayableSum,2), round(addPayableSum,2), round(payableSum,2), round(paymentSum,2)]

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
            return render_template('financial_othercosts.html', form=form, username=username, supplementarySuppliers=supplementarySuppliers, supplementaryPayableSum=supplementaryPayableSum, operationSelects=operationSelects, operations=operations, operationSum=operationSum, aftersales=aftersales, aftersaleSum=aftersaleSum, month=month, today=today)
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/add_supplementaries', methods=['POST'])
def add_supplementaries():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            supplementaries = data['supplementaries']  # supplierCode, inDate, supplementaryCode, inNum, price, money, remark
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            for i in supplementaries:
                thread = myThread(target=insert_supplementary,args=(i[0], i[2], i[1], i[3], i[4], i[6], entryTime, entryClerk,))

            # 返回数据
            thread = myThread(target=select_all_supplementarySuppliers, args=())
            suppliers = thread.get_result()
            month = entryTime[0:7]
            payables=[]
            remainPayableSum = 0
            addPayableSum = 0
            payableSum = 0
            paymentSum = 0
            for i in suppliers:
                thread = myThread(target=select_supplementaryPayableReportByCode, args=(i[0], month,)) # supplierCode,remainPayable,addPayable,payable,payment,remark
                payable = thread.get_result()
                payables.append(payable[0])

                remainPayableSum += payable[0][1]
                addPayableSum += payable[0][2]
                payableSum += payable[0][3]
                paymentSum += payable[0][4]
            supplementaryPayableSum = [remainPayableSum, addPayableSum, payableSum, paymentSum]
            return jsonify({'ok': True, 'payables': payables, 'supplementaryPayableSum': supplementaryPayableSum})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/delete_supplementaries', methods=['POST'])
def delete_supplementaries():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            supplierCodeArr = data['supplierCodeArr']  # 不要写成orderCode=request.data["orderCode"]
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            for i in supplierCodeArr:
                myThread(target=delete_supplementaryBySupplierCode, args=(i, entryTime, entryClerk, ))
            return jsonify({'ok': True})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/edit_supplementary/<supplierCode>', methods=['GET', 'POST'])
def edit_supplementary(supplierCode):
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username

            # 先删除
            thread = myThread(target=delete_supplementaryBySupplierCode,args=(supplierCode, entryTime, entryClerk,))

            # 后添加
            data = request.get_json()
            supplementaries = data['supplementaries']  # supplierCode, inDate, supplementaryCode, inNum, price, money, remark
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            payables = []
            for i in supplementaries:
                thread = myThread(target=insert_supplementary, args=(i[0], i[2], i[1], i[3], i[4], i[6], entryTime, entryClerk,))

            # 返回数据
            month = entryTime[0:7]
            thread = myThread(target=select_supplementaryPayableReportByCode, args=(supplierCode, month,))  # supplierCode,remainPayable,addPayable,payable,payment,remark
            payable = thread.get_result()
            thread = myThread(target=select_all_supplementarySuppliers, args=())
            suppliers = thread.get_result()
            remainPayableSum = 0
            addPayableSum = 0
            payableSum = 0
            paymentSum = 0
            for i in suppliers:
                thread = myThread(target=select_supplementaryPayableReportByCode, args=(i[0], month,))  # supplierCode,remainPayable,addPayable,payable,payment,remark
                payable = thread.get_result()
                payables.append(payable[0])

                remainPayableSum += payable[0][1]
                addPayableSum += payable[0][2]
                payableSum += payable[0][3]
                paymentSum += payable[0][4]
            supplementaryPayableSum = [remainPayableSum, addPayableSum, payableSum, paymentSum]
            return jsonify({'ok': True, 'payable': payable, 'supplementaryPayableSum': supplementaryPayableSum})
        elif request.method=="GET":
            thread = myThread(target=select_supplementaryByCode, args=(supplierCode,))
            supplementary=thread.get_result()
            return jsonify({'ok': True,'supplementary':supplementary})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/supplementary_payments/<supplierCode>', methods=['POST'])
def supplementary_payments(supplierCode):
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            supplierCode = data['supplierCode']  # 不要写成orderCode=request.data["orderCode"]
            beforePayable = float(data['beforePayable'])
            paymentDate = data['paymentDate']
            payment = float(data['payment'])
            remark = data['remark']
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            thread = myThread(target=insert_supplementaryPayments,args=(supplierCode, paymentDate, beforePayable, payment, remark, entryTime, entryClerk,))
            return jsonify({'ok': True})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/search_supplementary_supplier/<filterStr>', methods=['GET'])
def search_supplementary_supplier(filterStr):
    if session.get('username'):
        username = session['username']
        if request.method == "GET":
            thread = myThread(target=select_supplementarySupplierInfoByFilter, args=(filterStr,))  # client, address, contact, telephone
            suppliers = thread.get_result()
            return jsonify({'ok': True,'suppliers':suppliers})
    else:
        return jsonify({'ok': False})

# xijiawei
# 订单管理
@financial_app.route('/search_operation/<month>', methods=['GET'])
def search_operation(month):
    if session.get('username'):
        username = session['username']
        if request.method == "GET":
            thread = myThread(target=select_operationsByMonth,args=(month,))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operationArr = thread.get_result()
            thread = myThread(target=select_operationSumByMonth, args=(month,))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = thread.get_result()
            return jsonify({'ok': True,'operationArr':operationArr, 'operationSum': operationSum})
    else:
        return render_template('access_fail.html')

# xijiawei
# 按时间段查询运营费用（新）
@financial_app.route('/search_operationBySelect', methods=['POST'])
def search_operationBySelect():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            select = data['operationSelect']
            month = data['operationMonth']
            thread = myThread(target=select_operationsBySelect,args=(select, month,))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operationArr = thread.get_result()
            thread = myThread(target=select_operationSumBySelect, args=(select, month,))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = thread.get_result()
            return jsonify({'ok': True,'operationArr':operationArr, 'operationSum': operationSum})
    else:
        return render_template('access_fail.html')

# xijiawei
# 按时间段查询运营费用（新·加强）
@financial_app.route('/search_operationByDuration', methods=['POST'])
def search_operationByDuration():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            select = data['operationSelect']
            startMonth = data['operationStartMonth']
            endMonth = data['operationEndMonth']
            thread = myThread(target=select_operationsByDuration,args=(select, startMonth, endMonth,))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operationArr = thread.get_result()
            thread = myThread(target=select_operationSumByDuration, args=(select, startMonth, endMonth,))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = thread.get_result()
            return jsonify({'ok': True,'operationArr':operationArr, 'operationSum': operationSum})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/add_operations', methods=['POST'])
def add_operations():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            operations = data['operations']  # supplierCode, inDate, supplementaryCode, inNum, price, money, remark
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            for i in operations:
                if i[0]=="":
                    myThread(target=insert_operation,args=(i[1], i[2], i[3], entryTime, entryClerk,))
                else:
                    myThread(target=update_operation,args=(i[0], i[1], i[2], i[3], entryTime, entryClerk,))

            # 返回数据
            thread = myThread(target=select_operationSelect, args=())
            operationSelects = thread.get_result()
            thread = myThread(target=select_operationsByMonth,args=(entryTime[0:7],))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operationArr = thread.get_result()
            thread = myThread(target=select_operationSumByMonth, args=(entryTime[0:7],))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = thread.get_result()
            return jsonify({'ok': True, 'operationArr': operationArr, 'operationSum': operationSum, 'operationSelects': operationSelects})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/add_operationsBySelect', methods=['POST'])
def add_operationsBySelect():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            select = data['operationSelect']
            month = data['operationMonth']
            operations = data['operations']  # supplierCode, inDate, supplementaryCode, inNum, price, money, remark
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            for i in operations:
                if i[0]=="":
                    myThread(target=insert_operation,args=(i[1], i[2], i[3], entryTime, entryClerk,))
                else:
                    myThread(target=update_operation,args=(i[0], i[1], i[2], i[3], entryTime, entryClerk,))

            # 返回数据
            thread = myThread(target=select_operationSelect, args=())
            operationSelects = thread.get_result()
            thread = myThread(target=select_operationsBySelect,args=(select, month,))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operationArr = thread.get_result()
            thread = myThread(target=select_operationSumBySelect, args=(select, month,))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = thread.get_result()
            return jsonify({'ok': True, 'operationArr': operationArr, 'operationSum': operationSum, 'operationSelects': operationSelects})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/add_operationsInCondition', methods=['POST'])
def add_operationsInCondition():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            select = data['operationSelect']
            startMonth = data['operationStartMonth']
            endMonth = data['operationEndMonth']
            operations = data['operations']  # supplierCode, inDate, supplementaryCode, inNum, price, money, remark
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            for i in operations:
                if i[0]=="":
                    myThread(target=insert_operation,args=(i[1], i[2], i[3], entryTime, entryClerk,))
                else:
                    myThread(target=update_operation,args=(i[0], i[1], i[2], i[3], entryTime, entryClerk,))

            # 返回数据
            thread = myThread(target=select_operationSelect, args=())
            operationSelects = thread.get_result()
            thread = myThread(target=select_operationsByDuration,args=(select, startMonth, endMonth,))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operationArr = thread.get_result()
            thread = myThread(target=select_operationSumByDuration, args=(select, startMonth, endMonth,))  # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = thread.get_result()
            return jsonify({'ok': True, 'operationArr': operationArr, 'operationSum': operationSum, 'operationSelects': operationSelects})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/delete_operations', methods=['POST'])
def delete_operations():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            costCodeArr = data['costCodeArr']
            for i in costCodeArr:
                myThread(target=delete_operationByCode,args=(i, ))
            return jsonify({'ok': True})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/search_aftersale/<month>', methods=['GET'])
def search_aftersale(month):
    if session.get('username'):
        username = session['username']
        if request.method == "GET":
            thread = myThread(target=select_aftersalesByMonth,args=(month,))  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleArr = thread.get_result()
            thread = myThread(target=select_aftersaleSumByMonth, args=(month,))  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleSum = thread.get_result()
            return jsonify({'ok': True,'aftersaleArr':aftersaleArr, 'aftersaleSum': aftersaleSum})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/search_aftersaleByDuration', methods=['POST'])
def search_aftersaleByDuration():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            startMonth = data['aftersaleStartMonth']
            endMonth = data['aftersaleEndMonth']
            thread = myThread(target=select_aftersalesByDuration,args=(startMonth, endMonth,))  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleArr = thread.get_result()
            thread = myThread(target=select_aftersaleSumByDuration, args=(startMonth, endMonth,))  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleSum = thread.get_result()
            return jsonify({'ok': True,'aftersaleArr':aftersaleArr, 'aftersaleSum': aftersaleSum})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/add_aftersales', methods=['POST'])
def add_aftersales():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            month = data['aftersaleMonth']
            aftersales = data['aftersales']  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            for i in aftersales:
                if i[0]=="":
                    myThread(target=insert_aftersale,args=(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], entryTime, entryClerk,))
                else:
                    myThread(target=update_aftersale,args=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], entryTime, entryClerk,))

            # 返回数据
            thread = myThread(target=select_aftersalesByMonth,args=(month,))  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleArr = thread.get_result()
            thread = myThread(target=select_aftersaleSumByMonth, args=(month,))  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleSum = thread.get_result()
            return jsonify({'ok': True, 'aftersaleArr': aftersaleArr, 'aftersaleSum': aftersaleSum})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/add_aftersalesInCondition', methods=['POST'])
def add_aftersalesInCondition():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            startMonth = data['aftersaleStartMonth']
            endMonth = data['aftersaleEndMonth']
            aftersales = data['aftersales']  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            for i in aftersales:
                if i[0]=="":
                    myThread(target=insert_aftersale,args=(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], entryTime, entryClerk,))
                else:
                    myThread(target=update_aftersale,args=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], entryTime, entryClerk,))

            # 返回数据
            thread = myThread(target=select_aftersalesByDuration,args=(startMonth, endMonth,))  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleArr = thread.get_result()
            thread = myThread(target=select_aftersaleSumByDuration, args=(startMonth, endMonth,))  # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleSum = thread.get_result()
            return jsonify({'ok': True,'aftersaleArr':aftersaleArr, 'aftersaleSum': aftersaleSum})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/delete_aftersales', methods=['POST'])
def delete_aftersales():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            costCodeArr = data['costCodeArr']
            for i in costCodeArr:
                myThread(target=delete_aftersaleByCode,args=(i, ))
            return jsonify({'ok': True})
    else:
        return render_template('access_fail.html')

