from flask import render_template, request, session, Blueprint, jsonify

from db import *
from form import *

from datetime import datetime

order_app=Blueprint('order',__name__)

# xijiawei
# 订单管理
@order_app.route('/order', methods=['GET'])
def order():
    if session.get('username'):
        if request.method == "POST":
            print("")
        elif request.method=="GET":
            username = session['username']
            form = ProductForm()
            orders = select_concated_orders()
            return render_template('order.html', form=form, orders=orders, username=username)
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@order_app.route('/orders_in_month/<month>', methods=['GET'])
def orders_in_month(month):
    if session.get('username'):
        if request.method == "POST":
            print("")
        elif request.method=="GET":
            orders = select_concated_ordersByMonth(month)
            return jsonify({'ok': True, 'orders': orders})
    else:
        return render_template('access_fail.html')

# xijiawei
# 订单管理
@order_app.route('/add_order', methods=['POST'])
def add_order():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            orderCode = data['orderCode']  # 不要写成orderCode=request.data["orderCode"]
            clientCode = data['clientCode']
            orderDate = data['orderDate']
            productOfOrderArr = data['productOfOrderArr']
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            for product in productOfOrderArr:
                productType = product[0]
                uint = product[1]
                deliveryNum = product[2]
                price = product[3]
                receivable = product[4]
                deliveryDate = product[5]
                remark = product[6]
                myThread(target=insert_order, args=(orderCode, orderDate, clientCode, productType, deliveryNum, deliveryDate, uint, price, receivable, remark, entryTime, entryClerk,))
            return jsonify({'ok': True})
    else:
        return jsonify({'ok': False})

# xijiawei
# 订单管理
@order_app.route('/edit_order/<orderCode>', methods=['GET', 'POST'])
def edit_order(orderCode):
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            orderCode = data['orderCode']  # 不要写成orderCode=request.data["orderCode"]
            clientCode = data['clientCode']
            orderDate = data['orderDate']
            productOfOrderArr = data['productOfOrderArr']
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            # 清空旧订单
            myThread(target=delete_order, args=(orderCode,))
            # 插入新订单
            for product in productOfOrderArr:
                productType = product[0]
                unit = product[1]
                deliveryNum = product[2]
                price = product[3]
                receivable = product[4]
                deliveryDate = product[5]
                remark = product[6]
                myThread(target=insert_order, args=(orderCode, orderDate, clientCode, productType, deliveryNum, deliveryDate, unit, price, receivable, remark, entryTime, entryClerk,))
            return jsonify({'ok': True})
        elif request.method=="GET":
            productOfOrderArr = select_orderByCode(orderCode) # client, address, contact, telephone, orderDate, productType, deliveryNum, deliveryDate, deliveredNum, uint, price, receivable, remark
            return jsonify({'ok': True, 'productOfOrderArr': productOfOrderArr})
        else:
            return jsonify({'ok': False})
    else:
        return jsonify({'ok': False})

# xijiawei
# 删除订单
@order_app.route('/delete_orders', methods=['POST'])
def delete_orders():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            orderCodeArr = data['orderCodeArr']  # 不要写成orderCode=request.data["orderCode"]
            for orderCode in orderCodeArr:
                myThread(target=delete_order, args=(orderCode,))
            return jsonify({'ok': True})
    else:
        return jsonify({'ok': False})

# xijiawei
# 按订单出货（暂不用）
@order_app.route('/deliver/<orderCode>', methods=['GET', 'POST'])
def deliver(orderCode):
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            orderCode = data['orderCode']  # 不要写成orderCode=request.data["orderCode"]
            sendDate = data['sendDate']
            client = data['client']
            contact = data['contact']
            address = data['address']
            telephone = data['telephone']
            deliverProductArr = data['deliverProductArr']
            deliveryCode="D"+datetime.now().strftime('%Y%m%d%H%M%S%f')[0:16] # 使用时间戳生成唯一代号
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            products = []
            for product in deliverProductArr:
                productType = product[0]
                uint = product[1]
                sendNum = product[2]
                price = product[3]
                remark = product[4]
                productInfo = select_orderByCodeAndType(orderCode, productType)
                beforeDeliveryNum = productInfo[0][0]
                inventoryNum = productInfo[0][1]
                myThread(target=insert_delivery, args=(deliveryCode, orderCode, productType, beforeDeliveryNum, sendDate, sendNum, price, remark, client, client, address, contact, telephone, entryTime, entryClerk,))

                # 返回刷新数据
                productDeliverRecord=[]
                productDeliverRecord.append(productType)
                productDeliverRecord.append(deliveryCode)
                productDeliverRecord.append(sendDate)
                productDeliverRecord.append(sendNum)
                productDeliverRecord.append(beforeDeliveryNum)
                productDeliverRecord.append(beforeDeliveryNum-sendNum)
                productDeliverRecord.append(inventoryNum)
                productDeliverRecord.append(inventoryNum-sendNum)
                productDeliverRecord.append(remark)
                products.append(productDeliverRecord) # productType, deliveryCode, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, inventoryNum, inventoryNum-sendNum, remark
            return jsonify({'ok': True,'productOfOrderArr':products})
        elif request.method=="GET":
            # 方式一，sql连接，不适用：
            # thread = myThread(target=select_deliveryWithOrderByCode, args=(orderCode,))
            # productOfDeliverArr = thread.get_result()
            # productType = ''
            # products=[]
            # for i in productOfDeliverArr:
            #     if not i[0] == productType:
            #         productType = i[0]
            #         product = []
            #         deliverRecord = []
            #         product.append(i[0])  # productType
            #         product.append(i[1])  # deliveryNum
            #         product.append(i[2])  # deliveryDate
            #         if i[3] and i[4] and i[5] and i[6] and i[7] and i[8] and i[9]:
            #             deliverRecord.append([i[3],i[4],i[5], i[6], i[7], i[8], i[9]])  # deliveryCode, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, productInfo.inventoryNum, productInfo.inventoryNum-sendNum, delivery.remark
            #         else:
            #             deliverRecord.append(["","",""])
            #         product.append(deliverRecord)
            #         product.append(i[10])  # client
            #         product.append(i[11])  # orderDate
            #         # productType, deliveryNum, deliveryDate, [deliveryCode, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, productInfo.inventoryNum, productInfo.inventoryNum-sendNum, delivery.remark], client, address, telephone, account, orderDate, uint, price
            #         products.append(product)
            #     else:
            #         deliverRecord.append([i[3], i[4], i[5], i[6], i[7], i[8], i[9]])  # deliveryCode, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, productInfo.inventoryNum, productInfo.inventoryNum-sendNum, delivery.remark
            # 方式二：
            productOfOrderArr = select_orderByCode(orderCode) # client, address, contact, telephone, orderDate, productType, deliveryNum, deliveryDate, deliveredNum, uint, price, receivable, remark
            products = []
            for i in productOfOrderArr:
                product = []
                product.append(i[0])  # client
                product.append(i[1])  # address
                product.append(i[2])  # contact
                product.append(i[3])  # telephone
                product.append(i[4])  # orderDate
                product.append(i[5])  # productType
                product.append(i[6])  # deliveryNum
                product.append(i[7])  # deliveryDate
                # i[8] # deliveredNum
                product.append(i[9])  # uint
                product.append(i[10])  # price
                # i[11] # receivable
                # i[12] # remark
                deliverRecord = select_deliveryByOrderCodeAndProductType(orderCode, i[5]) # deliveryCode, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, productInfo.inventoryNum, productInfo.inventoryNum-sendNum, delivery.remark
                product.append(deliverRecord)
                product.append(i[8])  # orderDate
                # client, address, contact, telephone, orderDate, productType, deliveryNum, deliveryDate, uint, price, [deliveryCode, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, productInfo.inventoryNum, productInfo.inventoryNum-sendNum, delivery.remark]
                products.append(product)
            nowTime = datetime.now().strftime('%Y-%m-%d')
            return jsonify({'ok': True, 'productOfOrderArr': products, 'nowTime': nowTime, 'entryClerk': username})
        else:
            return jsonify({'ok': False})
    else:
        return jsonify({'ok': False})

# xijiawei
# 打印订单出货单（暂不用）
@order_app.route('/print_deliver/<deliveryCode>', methods=['GET'])
def print_deliver(deliveryCode):
    if session.get('username'):
        username = session['username']
        if request.method == "GET":
            deliverRecord = select_deliveryByCode(deliveryCode) # client, address, contact, telephone, orderDate, productType, deliveryNum, deliveryDate, uint, price, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, delivery.remark, delivery.entryClerk
            return jsonify({'ok': True,'productOfDeliverArr':deliverRecord})
    else:
        return jsonify({'ok': False})

# xijiawei
# 客户出货页面
@order_app.route('/deliverGroupByClient', methods=['GET'])
def deliverGroupByClient():
    if session.get('username'):
        if request.method=="GET":
            username = session['username']
            form = ProductForm()
            clients = select_all_orderGroupByProductType()
            return render_template('order_deliver.html', form=form, clients=clients, username=username)
    else:
        return render_template('access_fail.html')

# xijiawei
# 按客户出货
@order_app.route('/deliverGroupByProductType/<clientCode>', methods=['GET','POST'])
def deliverGroupByProductType(clientCode):
    if session.get('username'):
        username = session['username']
        if request.method=="POST":
            data = request.get_json()
            deliveryCode = data['deliveryCode']  # 不要写成orderCode=request.data["orderCode"]
            sendDate = data['sendDate']
            client = data['client']
            contact = data['contact']
            address = data['address']
            telephone = data['telephone']
            deliverProductArr = data['deliverProductArr']
            deliveryCode = "D" + datetime.now().strftime('%Y%m%d%H%M%S%f')[0:16]  # 使用时间戳生成唯一代号
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            products = []
            for product in deliverProductArr:
                productType = product[0]
                uint = product[1]
                sendNum = product[2]
                price = product[3]
                remark = product[4]
                productInfo = select_orderGroupByProductTypeByClientCodeAndProductType(clientCode, productType)
                beforeDeliveryNum = productInfo[0][0]
                beforeDeliveredNum = productInfo[0][1]
                beforeInventoryNum = productInfo[0][2]
                myThread(target=insert_deliveryGroupByProductType, args=(deliveryCode, clientCode, productType, beforeDeliveryNum, sendDate, sendNum, price, remark, client, address, contact, telephone, entryTime, entryClerk,))

                # 返回刷新数据
                productDeliverRecord = []
                productDeliverRecord.append(productType)
                # productDeliverRecord.append(beforeDeliveredNum + sendNum)
                productDeliverRecord.append(int(select_deliveryGroupByProductTypeSumByClientCode(clientCode, productType, entryTime[0:7])))
                productDeliverRecord.append(beforeInventoryNum - sendNum)
                productDeliverRecord.append(deliveryCode)
                productDeliverRecord.append(sendDate)
                productDeliverRecord.append(sendNum)
                productDeliverRecord.append(beforeDeliveryNum)
                productDeliverRecord.append(beforeDeliveryNum - sendNum)
                productDeliverRecord.append(remark)
                products.append(productDeliverRecord)  # productType, deliveredNum, inventoryNum, deliveryCode, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, remark
            return jsonify({'ok': True, 'productOfOrderArr': products})
        elif request.method=="GET":
            username = session['username']
            form = ProductForm()
            nowTime = datetime.now().strftime('%Y-%m-%d')
            month = nowTime[0:7]
            deliveryCode = "D" + datetime.now().strftime('%Y%m%d%H%M%S%f')[0:16]  # 使用时间戳生成唯一代号
            clientInfo = select_clientByCode(clientCode)
            productOfOrderArr = select_orderGroupByProductTypeByCode(clientCode)
            products = []
            for i in productOfOrderArr:
                product = []
                # product.append(i[0])  # productType
                # product.append(i[1])  # remainDeliveryNum
                # product.append(i[2])  # addDeliveryNum
                # product.append(i[3])  # deliveryNum
                # product.append(i[4])  # deliveredNum
                # product.append(i[5]) # inventoryNum
                # product.append(i[6])  # uint
                # product.append(i[7])  # price

                result = select_receivableReportGroupByProductTypeByClientCodeAndProductType(clientCode, i[0], month)
                product.append(i[0])  # productType
                product.append(result[0][0])  # remainDeliveryNum
                product.append(result[0][1])  # addDeliveryNum
                product.append(result[0][2])  # deliveryNum
                product.append(result[0][3])  # deliveredNum
                product.append(i[3]) # inventoryNum
                product.append(i[1])  # uint
                product.append(i[2])  # price

                deliverRecord = select_deliveryGroupByProductTypeByClientCodeAndProductType(clientCode, i[0], month) # deliveryCode, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, remark
                product.append(deliverRecord)
                # productType, remainDeliveryNum, addDeliveryNum, deliveryNum, deliveredNum, inventoryNum, uint, price, [deliveryCode, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, remark]
                products.append(product)
            return jsonify({'ok': True, 'deliveryCode': deliveryCode, 'client': clientInfo, 'productOfOrderArr': products, 'nowTime': nowTime, 'entryClerk': username})
    else:
        return render_template('access_fail.html')

# xijiawei
# 打印客户出货单
@order_app.route('/print_deliveryGroupByProductType/<deliveryCode>', methods=['GET'])
def print_deliveryGroupByProductType(deliveryCode):
    if session.get('username'):
        username = session['username']
        if request.method == "GET":
            deliverRecord = select_deliveryGroupByProductTypeByCode(deliveryCode) # client, address, contact, telephone, sendDate, productType, uint, price, sendNum, delivery.remark, delivery.entryClerk
            return jsonify({'ok': True,'productOfDeliverArr':deliverRecord})
    else:
        return jsonify({'ok': False})

# xijiawei
# 查询客户出货记录
@order_app.route('/deliveryGroupByProductTypeGroupByDeliveryCode/<clientCode>', methods=['GET','POST'])
def deliveryGroupByProductTypeGroupByDeliveryCode(clientCode):
    if session.get('username'):
        username = session['username']
        if request.method=="GET":
            username = session['username']
            form = ProductForm()
            clientInfo = select_clientByCode(clientCode)
            deliveryRecordOfOrderArr = select_deliveryGroupByProductTypeByClientCode(clientCode)
            deliveries = []
            delivery = []
            product = []
            deliveryCode = ''
            for i in deliveryRecordOfOrderArr:
                if not deliveryCode==i[0]:
                    deliveryCode = i[0]
                    delivery = []
                    product = []
                    delivery.append(i[0])
                    delivery.append(i[1])
                    product.append([i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]])
                    delivery.append(product)
                    deliveries.append(delivery)
                else:
                    product.append([i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]])
            nowTime = datetime.now().strftime('%Y-%m-%d')
            return jsonify({'ok': True, 'client': clientInfo, 'deliveries': deliveries, 'nowTime': nowTime, 'entryClerk': username})
    else:
        return render_template('access_fail.html')

# xijiawei
# 删除订单
@order_app.route('/delete_deliveryGroupByProductTypes', methods=['POST'])
def delete_deliveryGroupByProductTypes():
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            deliveryCodeArr = data['deliveryCodeArr']  # 不要写成orderCode=request.data["orderCode"]
            for deliveryCode in deliveryCodeArr:
                myThread(target=delete_deliveryGroupByProductType, args=(deliveryCode,))
            return jsonify({'ok': True})
    else:
        return jsonify({'ok': False})

# xijiawei
# 订单管理
@order_app.route('/search_client/<filterStr>', methods=['GET'])
def search_client(filterStr):
    if session.get('username'):
        username = session['username']
        if request.method == "GET":
            clients = select_clientInfoByFilter(filterStr) # client, address, contact, telephone
            return jsonify({'ok': True,'clients':clients})
    else:
        return jsonify({'ok': False})
