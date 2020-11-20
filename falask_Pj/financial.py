from flask import render_template, request, session, Blueprint, jsonify

from db import *
from form import *

from datetime import datetime

financial_app=Blueprint('financial',__name__)

##### 收款记账 #####

# xijiawei
# 订单管理
@financial_app.route('/financial_receivable', methods=['GET', 'POST'])
def financial_receivable():
    if session.get('username'):
        if request.method=="POST":
            month = datetime.now().strftime('%Y-%m')
            clients = select_all_clients()
            receivables = []
            remainReceivableSum = 0
            addReceivableSum = 0
            receivableSum = 0
            receiptSum = 0
            for i in clients:
                receivable = []
                result = select_receivableReportByCode(i[0], month)
                receivable.append(result[0][0])
                receivable.append(i[1]) # historyReceivable
                receivable.append(result[0][1])
                receivable.append(result[0][2])
                receivable.append(result[0][3])
                receivable.append(result[0][4])
                receivable.append(round(result[0][3]-result[0][4],2))
                receivable.append(result[0][5])
                receivables.append(receivable)

                remainReceivableSum += result[0][1]
                addReceivableSum += result[0][2]
                receivableSum += result[0][3]
                receiptSum += result[0][4]
            sum = [round(remainReceivableSum,2), round(addReceivableSum,2), round(receivableSum,2), round(receiptSum,2), round(receivableSum-receiptSum,2)]
            return jsonify({'ok': True, 'sum': sum, 'receivables': receivables})
        elif request.method=="GET":
            username = session['username']
            form = ProductForm()

            month = datetime.now().strftime('%Y-%m')
            clients = select_all_clients()
            receivables = []
            remainReceivableSum = 0
            addReceivableSum = 0
            receivableSum = 0
            receiptSum = 0
            for i in clients:
                receivable = []
                result = select_receivableReportByCode(i[0], month)
                receivable.append(result[0][0])
                receivable.append(i[1]) # historyReceivable
                receivable.append(result[0][1])
                receivable.append(result[0][2])
                receivable.append(result[0][3])
                receivable.append(result[0][4])
                receivable.append(round(result[0][3]-result[0][4],2))
                receivable.append(result[0][5])
                receivables.append(receivable)

                remainReceivableSum += result[0][1]
                addReceivableSum += result[0][2]
                receivableSum += result[0][3]
                receiptSum += result[0][4]
            sum = [round(remainReceivableSum,2), round(addReceivableSum,2), round(receivableSum,2), round(receiptSum,2), round(receivableSum-receiptSum,2)]
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
            receipts = select_receiptsJournal(clientCode)
            receiptSum = select_receiptsJournalSum(clientCode)
            return jsonify({'ok': True, 'receipts': receipts, 'receiptSum': receiptSum})
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

# xijiawei
# 订单管理
@financial_app.route('/financial_delete_receipt/<receiptCode>', methods=['POST'])
def financial_delete_receipt(receiptCode):
    if session.get('username'):
        username = session['username']
        if request.method=="POST":
            myThread(target=delete_receiptsJournal, args=(receiptCode,))
            return jsonify({'ok': True})
    else:
        return render_template('access_fail.html')

##### 付款记账 #####

# xijiawei
# 订单管理
@financial_app.route('/financial_payable', methods=['GET', 'POST'])
def financial_payable():
    if session.get('username'):
        if request.method=="POST":
            month = datetime.now().strftime('%Y-%m')
            suppliers = select_all_suppliers()
            payables = []
            remainPayableSum = 0
            addPayableSum = 0
            payableSum = 0
            paymentSum = 0
            for i in suppliers:
                payable = []
                result = select_payableReportByCode(i[0], month)
                payable.append(result[0][0])
                payable.append(i[1]) # historyPayable
                payable.append(result[0][1])
                payable.append(result[0][2])
                payable.append(result[0][3])
                payable.append(result[0][4])
                payable.append(round(result[0][3]-result[0][4],2))
                payable.append(result[0][5])
                payables.append(payable)

                remainPayableSum += result[0][1]
                addPayableSum += result[0][2]
                payableSum += result[0][3]
                paymentSum += result[0][4]
            sum = [round(remainPayableSum,2), round(addPayableSum,2), round(payableSum,2), round(paymentSum,2), round(payableSum-paymentSum,2)]
            return jsonify({'ok': True, 'sum': sum, 'payables': payables})
        elif request.method=="GET":
            username = session['username']
            form = ProductForm()

            month = datetime.now().strftime('%Y-%m')
            suppliers = select_all_suppliers()
            payables = []
            remainPayableSum = 0
            addPayableSum = 0
            payableSum = 0
            paymentSum = 0
            for i in suppliers:
                payable = []
                result = select_payableReportByCode(i[0], month)
                payable.append(result[0][0])
                payable.append(i[1]) # historyPayable
                payable.append(result[0][1])
                payable.append(result[0][2])
                payable.append(result[0][3])
                payable.append(result[0][4])
                payable.append(round(result[0][3]-result[0][4],2))
                payable.append(result[0][5])
                payables.append(payable)

                remainPayableSum += result[0][1]
                addPayableSum += result[0][2]
                payableSum += result[0][3]
                paymentSum += result[0][4]
            sum = [round(remainPayableSum,2), round(addPayableSum,2), round(payableSum,2), round(paymentSum,2), round(payableSum-paymentSum,2)]
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
            payments = select_paymentsJournal(supplierCode)
            paymentSum = select_paymentsJournalSum(supplierCode)
            return jsonify({'ok': True, 'payments': payments, 'paymentSum': paymentSum})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/search_supplier/<filterStr>', methods=['GET'])
def search_supplier(filterStr):
    if session.get('username'):
        username = session['username']
        if request.method == "GET":
            suppliers = select_supplierInfoByFilter(filterStr) # client, address, contact, telephone
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

# xijiawei
# 订单管理
@financial_app.route('/financial_delete_payment/<paymentCode>', methods=['POST'])
def financial_delete_payment(paymentCode):
    if session.get('username'):
        username = session['username']
        if request.method=="POST":
            myThread(target=delete_paymentsJournal, args=(paymentCode,))
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
            authority = select_user_authority(username)
            form = ProductForm()

            month=datetime.now().strftime('%Y-%m')
            # workerSalary = select_all_workerSalary()
            # managerSalary = select_all_managerSalary()
            # workerSalarySum = select_workerSalarySumThisMonth()
            # managerSalarySum = select_managerSalarySumThisMonth()
            workerSalary = select_workerSalaryRecordByMonth(month)
            managerSalary = select_managerSalaryRecordByMonth(month)
            workerSalarySum = select_workerSalarySumByMonth(month)
            managerSalarySum = select_managerSalarySumByMonth(month)
            return render_template('financial_salary.html', form=form, username=username, authority=authority[1], workerSalary=workerSalary, managerSalary=managerSalary, workerSalarySum=workerSalarySum, managerSalarySum=managerSalarySum, month=month)
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/workersalary_in_moth/<month>', methods=['GET'])
def workersalary_in_moth(month):
    if session.get('username'):
        if request.method == "POST":
            print("")
        elif request.method=="GET":
            username = session['username']

            workerSalary = select_workerSalaryRecordByMonth(month)
            workerSalarySum = select_workerSalarySumByMonth(month)
            return jsonify({'ok': True, 'workerSalary': workerSalary, 'workerSalarySum': workerSalarySum})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@financial_app.route('/managersalary_in_moth/<month>', methods=['GET'])
def managersalary_in_moth(month):
    if session.get('username'):
        if request.method == "POST":
            print("")
        elif request.method=="GET":
            username = session['username']

            managerSalary = select_managerSalaryRecordByMonth(month)
            managerSalarySum = select_managerSalarySumByMonth(month)
            return jsonify({'ok': True, 'managerSalary': managerSalary, 'managerSalarySum': managerSalarySum})
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
            month = data['month']
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
            thread=myThread(target=insert_workerSalary, args=(month, name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk,))
            staffid = thread.get_result()
            return jsonify({'ok': True, 'staffid': staffid})
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
            salaryArr = select_all_workerSalary()
            result = select_workerSalarySumByMonth(month)[0]
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
            month = data['month']
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
            thread=myThread(target=insert_managerSalary, args=(month, name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk,))
            staffid = thread.get_result()
            return jsonify({'ok': True, 'staffid': staffid})
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

            salaryArr = select_all_managerSalary()
            result = select_managerSalarySumByMonth(month)[0]
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

            suppliers = select_all_supplementarySuppliers()
            today = datetime.now().strftime('%Y-%m-%d')
            month = datetime.now().strftime('%Y-%m')
            supplementarySuppliers=[]
            remainPayableSum = 0
            addPayableSum = 0
            payableSum = 0
            paymentSum = 0
            for i in suppliers:
                payable = select_supplementaryPayableReportByCode(i[0], month) # supplierCode,remainPayable,addPayable,payable,payment,remark
                supplementarySuppliers.append(payable[0])

                remainPayableSum += payable[0][1]
                addPayableSum += payable[0][2]
                payableSum += payable[0][3]
                paymentSum += payable[0][4]
            supplementaryPayableSum = [round(remainPayableSum,2), round(addPayableSum,2), round(payableSum,2), round(paymentSum,2)]

            operationSelects = select_operationSelect()
            operations = select_operationsByMonth(month) # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = select_operationSumByMonth(month)

            aftersales = select_aftersalesByMonth(month) # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleSum = select_aftersaleSumByMonth(month) # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
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
            suppliers = select_all_supplementarySuppliers()
            month = entryTime[0:7]
            payables=[]
            remainPayableSum = 0
            addPayableSum = 0
            payableSum = 0
            paymentSum = 0
            for i in suppliers:
                payable = select_supplementaryPayableReportByCode(i[0], month) # supplierCode,remainPayable,addPayable,payable,payment,remark
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
            myThread(target=delete_supplementaryBySupplierCode,args=(supplierCode, entryTime, entryClerk,))

            # 后添加
            data = request.get_json()
            supplementaries = data['supplementaries']  # supplierCode, inDate, supplementaryCode, inNum, price, money, remark
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            payables = []
            for i in supplementaries:
                myThread(target=insert_supplementary, args=(i[0], i[2], i[1], i[3], i[4], i[6], entryTime, entryClerk,))

            # 返回数据
            month = entryTime[0:7]
            suppliers = select_all_supplementarySuppliers()
            remainPayableSum = 0
            addPayableSum = 0
            payableSum = 0
            paymentSum = 0
            for i in suppliers:
                payable = select_supplementaryPayableReportByCode(i[0], month) # supplierCode,remainPayable,addPayable,payable,payment,remark
                payables.append(payable[0])

                remainPayableSum += payable[0][1]
                addPayableSum += payable[0][2]
                payableSum += payable[0][3]
                paymentSum += payable[0][4]
            supplementaryPayableSum = [remainPayableSum, addPayableSum, payableSum, paymentSum]
            return jsonify({'ok': True, 'payables': payables, 'supplementaryPayableSum': supplementaryPayableSum})
        elif request.method=="GET":
            supplementary = select_supplementaryByCode(supplierCode)
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
            myThread(target=insert_supplementaryPayments,args=(supplierCode, paymentDate, beforePayable, payment, remark, entryTime, entryClerk,))
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
            suppliers = select_supplementarySupplierInfoByFilter(filterStr) # client, address, contact, telephone
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
            operationArr = select_operationsByMonth(month) # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = select_operationSumByMonth(month)
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
            operationArr = select_operationsBySelect(select, month) # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = select_operationSumBySelect(select, month) # costCode, costDate, cost, remark, entryTime, entryClerk
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
            operationArr = select_operationsByDuration(select, startMonth, endMonth) # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = select_operationSumByDuration(select, startMonth, endMonth) # costCode, costDate, cost, remark, entryTime, entryClerk
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
            operationSelects = select_operationSelect()
            operationArr = select_operationsByMonth(entryTime[0:7]) # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = select_operationSumByMonth(entryTime[0:7])
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
            operationSelects = select_operationSelect()
            operationArr = select_operationsBySelect(select, month) # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = select_operationSumBySelect(select, month) # costCode, costDate, cost, remark, entryTime, entryClerk
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
            operationSelects = select_operationSelect()
            operationArr = select_operationsByDuration(select, startMonth, endMonth) # costCode, costDate, cost, remark, entryTime, entryClerk
            operationSum = select_operationSumByDuration(select, startMonth, endMonth) # costCode, costDate, cost, remark, entryTime, entryClerk
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
            aftersaleArr = select_aftersalesByMonth(month) # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleSum = select_aftersaleSumByMonth(month) # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
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
            aftersaleArr = select_aftersalesByDuration(startMonth, endMonth) # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleSum = select_aftersaleSumByDuration(startMonth, endMonth) # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
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
            aftersaleArr = select_aftersalesByMonth(month) # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleSum = select_aftersaleSumByMonth(month) # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
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
            aftersaleArr = select_aftersalesByDuration(startMonth, endMonth) # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
            aftersaleSum = select_aftersaleSumByDuration(startMonth, endMonth) # costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk
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

