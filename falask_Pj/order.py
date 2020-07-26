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
            thread = myThread(target=select_concated_orders, args=())
            orders = thread.get_result()
            return render_template('order.html', form=form, orders=orders, username=username)
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
            client = data['client']
            orderDate = data['orderDate']
            productOfOrderArr = data['productOfOrderArr']
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            for product in productOfOrderArr:
                productType=product[0]
                deliveryNum=product[1]
                deliveryDate=product[2]
                deliveredNum=0
                remark=product[3]
                myThread(target=insert_order, args=(orderCode, productType, deliveryNum, deliveryDate, deliveredNum, client, orderDate, remark, entryTime, entryClerk,))
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
            client = data['client']
            orderDate = data['orderDate']
            productOfOrderArr = data['productOfOrderArr']
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            entryClerk = username
            # 清空旧订单
            myThread(target=delete_order, args=(orderCode,))
            # 插入新订单
            for product in productOfOrderArr:
                productType = product[0]
                deliveryNum = product[1]
                deliveryDate = product[2]
                deliveredNum = 0
                remark = product[3]
                myThread(target=insert_order, args=(orderCode, productType, deliveryNum, deliveryDate, deliveredNum, client, orderDate, remark, entryTime, entryClerk,))
            return jsonify({'ok': True})
        elif request.method=="GET":
            thread = myThread(target=select_orderByCode, args=(orderCode,)) # productType, deliveryNum, deliveryDate, deliveredNum, client, orderDate, remark
            productOfOrderArr = thread.get_result()
            return jsonify({'ok': True, 'productOfOrderArr': productOfOrderArr})
        else:
            return jsonify({'ok': False})
    else:
        return jsonify({'ok': False})

# xijiawei
# 订单管理
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
# 订单管理
@order_app.route('/deliver/<orderCode>', methods=['GET', 'POST'])
def deliver(orderCode):
    if session.get('username'):
        username = session['username']
        if request.method == "POST":
            data = request.get_json()
            orderCode = data['orderCode']  # 不要写成orderCode=request.data["orderCode"]
            sendDate = data['sendDate']
            client = data['client']
            address = data['address']
            telephone = data['telephone']
            account = data['account']
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
                thread = myThread(target=select_orderByCodeAndType, args=(orderCode, productType,))
                productInfo = thread.get_result()
                beforeDeliveryNum = productInfo[0][0]
                inventoryNum = productInfo[0][1]
                myThread(target=insert_deliver, args=(deliveryCode, orderCode, productType, uint, price, beforeDeliveryNum, sendDate, sendNum, remark, client, address, telephone, account, entryTime, entryClerk,))

                # 更新orders
                myThread(target=update_order, args=(orderCode, productType, sendNum, client, address, telephone, account))

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
            # thread = myThread(target=select_deliverWithOrderByCode, args=(orderCode,))
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
            thread = myThread(target=select_orderByCode, args=(orderCode,)) # productType, deliveryNum, deliveryDate, deliveredNum, client, address, telephone, account, orderDate, remark, uint, price
            productOfOrderArr = thread.get_result()
            products = []
            for i in productOfOrderArr:
                product = []
                product.append(i[0])  # productType
                product.append(i[1])  # deliveryNum
                product.append(i[2])  # deliveryDate
                thread = myThread(target=select_deliversByOrderCode, args=(orderCode,i[0],))  # deliveryCode, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, productInfo.inventoryNum, productInfo.inventoryNum-sendNum, delivery.remark
                deliverRecord = thread.get_result()
                product.append(deliverRecord)
                product.append(i[4])  # client
                product.append(i[5])  # address
                product.append(i[6])  # telephone
                product.append(i[7])  # account
                product.append(i[8])  # orderDate
                # i[9] # remark
                product.append(i[10])  # uint
                product.append(i[11])  # price
                # productType, deliveryNum, deliveryDate, [deliveryCode, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, productInfo.inventoryNum, productInfo.inventoryNum-sendNum, delivery.remark], client, address, telephone, account, orderDate, uint, price
                products.append(product)
            nowTime = datetime.now().strftime('%Y-%m-%d')
            return jsonify({'ok': True, 'productOfOrderArr': products, 'nowTime': nowTime, 'entryClerk': username})
        else:
            return jsonify({'ok': False})
    else:
        return jsonify({'ok': False})

# xijiawei
# 订单管理
@order_app.route('/print_deliver/<deliveryCode>', methods=['GET'])
def print_deliver(deliveryCode):
    if session.get('username'):
        username = session['username']
        if request.method == "GET":
            thread = myThread(target=select_deliverByCode, args=(deliveryCode,))  # productType, deliveryNum, deliveryDate, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, productInfo.inventoryNum, productInfo.inventoryNum-sendNum, delivery.remark, client, address, telephone, account, orderDate, uint, price, delivery.entryClerk
            deliverRecord = thread.get_result()
            return jsonify({'ok': True,'productOfDeliverArr':deliverRecord})
    else:
        return jsonify({'ok': False})
