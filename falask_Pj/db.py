import threading
import pymysql

import uuid
from datetime import datetime

# 同步锁
lock=threading.Lock()

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="test", charset="utf8")
cur = conn.cursor()
# class dbHelper:
#     def __init__(self):
#         self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="test", charset="utf8")
#
#     def connect(self):
#         self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="test", charset="utf8")
#
#     def query(self, sql):
#         try:
#             cursor = self.conn.cursor()
#             cursor.execute(sql)
#         except pymysql.OperationalError:
#             self.connect()
#             cursor = self.conn.cursor()
#             cursor.execute(sql)
#         return cursor
# db = dbHelper()

# xijiawei
class dbHelper(object):
    def __init__(self, host=None, port=None, user=None, passwd=None, db=None, charset=None):
        self.pool = {}
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset

    def conn(self, ):
        name = threading.current_thread().name
        if name not in self.pool:
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset=self.charset)
            self.pool[name] = conn
        if self.pool[name]._closed:
            self.pool[name]=pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset=self.charset)
        return self.pool[name]
db = dbHelper(host="127.0.0.1", port=3306, user="root", passwd="123456", db="test", charset="utf8")

class myThread:
    def __init__(self, target, args):
        threading.Thread.__init__(self)
        self.target = target
        self.args = args
        self.result = self.target(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

# xijiawei
# 管理员_人员管理_查看人员
def select_all_users():
    sql = "select * from users;"
    # print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    return result
    conn.close()

# xijiawei
# 管理员_人员管理_查看人员
def select_all_users_for_selector():
    sql = "select userid,username from users;"
    # print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    return result
    conn.close()

# xijiawei
def select_user(username):
    sql = "select * from users where username='%s';"%username
    # print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    return result
    conn.close()

# xijiawei
def login_check(username,password):
    sql = "select * from users where username='%s' and password='%s';"%(username,password)
    # print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result[0][0]
    else:
        return None
    conn.close()

# xijiawei
def select_user_password(username):
    sql = "select password from users where username='%s';"%username
    # print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result[0][0]
    else:
        return None
    conn.close()

# xijiawei
def select_user_authority(username):
    sql = "select authority from users where username='%s';"%username
    # print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result[0][0]
    else:
        return None
    conn.close()

# xijiawei
def insert_user(username, password, authority):
    sql = "insert into users (username, password, authority) value('%s','%s','%s');" % (username, password, authority)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except Exception as e:
        print("插入异常：", e)
        conn.rollback()

# xijiawei
def update_user_authority(userid, authority):
    sql = "update users set authority='%s' where userid='%s';"% (authority, userid)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except Exception as e:
        print("插入异常：", e)
        conn.rollback()

# xijiawei
def update_user_password(username, password):
    sql = "update users set password='%s' where username='%s';"% (password, username)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except Exception as e:
        print("插入异常：", e)
        conn.rollback()

# xijiawei
def delete_userByID(userid):
    sql = "delete from users where userid='%s';"%userid
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except Exception as e:
        print("插入异常：", e)
        conn.rollback()

# xijiawei
# 展示所有成品
def select_all_products():
    sql = "select productCode,productType,client,price,profit,totalCost,remark,entryTime,entryClerk from productInfo;"
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 根据成品编码查询成品录入信息
def select_productChangeByCode(productCode):
    sql = "select entryClerk,updateOfContent,isUpdateOrAdd,entryTime from productChange where productCode='%s';" % (productCode)
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 根据成品编码查询成品信息
def select_productInfoByCode(productCode):
    sql = "select productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk from productInfo where productCode='%s';"%(productCode)
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 根据成品编码查询成品物料组成
def select_materialsOfProductByCode(productCode):
    try:
        sql = "select mOP.materialCode,m.materialName,m.materialType,mOP.materialNum,mOP.materialPrice,mOP.materialCost,mOP.patchPoint,mOP.patchPrice,mOP.patchCost from materialsOfProduct mOP,materialInfo m where productCode='%s' and mOP.materialCode=m.materialCode;" % (
            productCode)
        cur.execute(sql)
        result = cur.fetchall()
        return result
        conn.close()
    except Exception as e:
        print("删除异常：",e)
        conn.close()
        conn.rollback()

# xijiawei
# 根据多个成品编码汇总物料
def select_materialsOfProductByCodeArr(productCodeArr):
    try:
        length = len(productCodeArr)
        if length == 0:
            return
        else:
            # sql="select m.materialCode,materialInfo.materialName,materialInfo.unit,materialInfo.inventoryNum,m.sum,materialInfo.inventoryNum-m.sum,materialInfo.supplier from (select materialInfo.materialCode,sum(materialsOfProduct.materialNum) sum from materialsOfProduct left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where materialsOfProduct.productCode='%s'"%productCodeArr[0]
            sql = "select m.materialCode,materialInfo.materialName,materialInfo.materialType,materialInfo.unit,materialInfo.inventoryNum,cast(m.sum as signed integer),cast(materialInfo.inventoryNum-m.sum as signed integer),materialInfo.supplier from (select materialInfo.materialCode,sum(materialsOfProduct.materialNum*productInfo.productNum) sum from materialsOfProduct left join productInfo on materialsOfProduct.productCode=productInfo.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where materialsOfProduct.productCode='%s'" % \
                  productCodeArr[0]
            for productCode in productCodeArr[1:productCodeArr.__len__()]:
                sql += " or materialsOfProduct.productCode='%s'" % productCode
            sql += " group by materialInfo.materialCode) m,materialInfo where materialInfo.materialCode=m.materialCode;"
            print(sql)
        conn.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        return result
        conn.close()
    except Exception as e:
        print("删除异常：",e)
        conn.close()
        conn.rollback()

# xijiawei
# 根据成品型号查询成品编码
def select_productCodeByType(productType):
    sql = "select productCode from productInfo where productType='%s';"%(productType)
    conn.ping(reconnect=True)
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 根据成品编码查询成品型号
def select_productTypeByCode(productCode):
    #global lock
    try:
        sql = "select productType from productInfo where productCode='%s';" % (productCode)
        conn.ping(reconnect=True)
        #lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        #lock.release()
        return result
    except Exception as e:
        print("删除异常：",e)
        conn.close()
        conn.rollback()
        #lock.release()
    finally:
        print("查询型号")

# xijiawei
# 根据成品编码查询成品其他成本组成信息
def select_otherCostsByCode(productCode):
    try:
        sql = "select processCost,adminstrationCost,supplementaryCost,operationCost,process, adminstration, supplementary, operation from otherCosts where productCode='%s';" % (
            productCode)
        cur.execute(sql)
        result = cur.fetchall()
        return result
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 插入成品
def insert_productInfo(productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk):
    sql = "insert into productInfo (productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk)value('%s','%s','%s','%f','%f','%f','%f','%f','%f','%f','%f','%f','%s','%s','%s');" \
          % (productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 插入成品：部分修改权限
def insert_productInfoInPart(productCode,productType,client,totalCost,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk):
    sql = "insert into productInfo (productCode,productType,client,totalCost,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk)value('%s','%s','%s','%f','%f','%f','%f','%f','%f','%s','%s','%s');" \
          % (productCode,productType,client,totalCost,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 更新成品静态表的productNum字段
def update_productNumOfProductInfo(productCode,productNum):
    sql = "update productInfo set productNum='%d' where productCode='%s';" \
          % (productNum,productCode)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 插入成品物料组成
def insert_materialsOfProduct(productCode,materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost):
    sql = "insert into materialsOfProduct (productCode,materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost) value('%s','%s','%d','%f','%f','%d','%f','%f');" \
          % (productCode,materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 插入成品其他成本组成
def insert_otherCosts(productCode,processCost,adminstrationCost,supplementaryCost,operationCost,process, adminstration, supplementary, operation):
    sql = "insert into otherCosts (productCode,processCost,adminstrationCost,supplementaryCost,operationCost,process, adminstration, supplementary, operation) value('%s','%f','%f','%f','%f','%s','%s','%s','%s');" \
          % (productCode,processCost,adminstrationCost,supplementaryCost,operationCost,process, adminstration, supplementary, operation)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except Exception as e:
        print("插入异常：", e)
        conn.rollback()

# xijiawei
# 插入成品录入表
def insert_productChange(productCode,entryClerk,updateOfContent,entryDate):
    # entryDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    sql = "insert into productChange (productCode,entryClerk,updateOfContent,entryDate) value('%s','%s','%s','%s');" \
          % (productCode,entryClerk,updateOfContent,entryDate)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 更新成品
def update_productInfo(productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk):
    sql = "update productInfo set productType='%s',client='%s',price='%f',profit='%f',totalCost='%f',taxRate='%f',materialCost='%f',processCost='%f',adminstrationCost='%f',supplementaryCost='%f',operatingCost='%f',remark='%s',entryTime='%s',entryClerk='%s' where productCode='%s';" \
          % (productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk,productCode)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 更新成品
def update_productInfoInPart(productCode,productType,client,totalCost,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk):
    sql = "update productInfo set productType='%s',client='%s',totalCost='%f',materialCost='%f',processCost='%f',adminstrationCost='%f',supplementaryCost='%f',operatingCost='%f',remark='%s',entryTime='%s',entryClerk='%s' where productCode='%s';" \
          % (productType,client,totalCost,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk,productCode)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 删除成品
def delete_productInfo(productCode):
    sql = "delete from productInfo where productCode='%s';" \
          % (productCode)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("删除异常：",e)
        conn.rollback()

# xijiawei
# 根据成品编码更新成品物料组成
def update_materialsOfProduct(productCode,materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost):
    sql = "update materialsOfProduct set materialNum='%d',materialPrice='%f',materialCost='%f',patchPoint='%d',patchPrice='%f',patchCost='%f' where productCode='%s' and materialCode='%s';" \
          % (materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost,productCode,materialCode)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 根据成品编码删除成品物料组成
def delete_materialsOfProduct(productCode):
    sql = "delete from materialsOfProduct where productCode='%s';" \
          % (productCode)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("删除异常：",e)
        conn.rollback()

# xijiawei
# 根据成品编码删除成品其他成本组成
def delete_otherCosts(productCode):
    sql = "delete from otherCosts where productCode='%s';" \
          % (productCode)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("删除异常：",e)
        conn.rollback()

# xijiawei
# 检查物料组成表
def check_materialsOfProduct(productCode,materialCode):
    conn=db.conn()
    cursor=conn.cursor()
    sql = "select * from materialsOfProduct where productCode= '%s' and materialCode='%s';"% (productCode,materialCode)
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result

# xijiawei
# 根据成品编码检查成品表
def check_productInfoByCode(productCode):
    conn=db.conn()
    cursor=conn.cursor()
    sql = "select * from productInfo where productCode= '%s';"% (productCode)
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result

# xijiawei
# 根据成品型号检查成品表
def check_productInfoByType(productType):
    conn=db.conn()
    cursor=conn.cursor()
    sql = "select * from productInfo where productType= '%s';"% (productType)
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result

# xijiawei
# 检查物料表
def check_materialInfo(materialCode):
    conn=db.conn()
    cursor=conn.cursor()
    sql = "select * from materialInfo where materialCode= '%s';"% (materialCode)
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result

# xijiawei
# 查询所有采购
def select_procurement():
    # entryDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    # sql = "select id,group_concat(productCode),group_concat(productType),group_concat(productNum),group_concat(client),group_concat(entryClerk),group_concat(entryDate) from procurement group by id;"
    sql = "select p2.count,p1.* from (select p.*,productInfo.productType,procurement.productNum,procurement.client,procurement.entryClerk,procurement.entryTime from (select t.*,group_concat(materialsOfProduct.materialCode),group_concat(materialInfo.materialName),group_concat(materialsOfProduct.materialNum) from (select procurement.procurementCode,procurement.productCode from procurement left join productInfo on procurement.productCode=productInfo.productCode) t left join materialsOfProduct on t.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode group by t.procurementCode,t.productCode) p,procurement,productInfo where p.procurementCode=procurement.procurementCode and p.productCode=procurement.productCode and p.productCode=productInfo.productCode order by procurement.entryTime) p1 left join (select count(procurementCode) count,procurementCode from procurement group by procurementCode) p2 on p1.procurementCode=p2.procurementCode;"
    try:
        cur.execute(sql)
        result = cur.fetchall()
        return result
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 根据采购代号查询采购
def select_procurementByCode(procurementCode):
    sql = "select p.productCode,productInfo.productType,p.productNum,p.client,p.remark,materialsOfProduct.materialCode,materialInfo.materialName,materialInfo.materialType,materialsOfProduct.materialNum from procurement p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s';"%(procurementCode)
    try:
        cur.execute(sql)
        result = cur.fetchall()
        return result
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 根据采购代号汇总采购物料
def select_materialsOfProcurementByCode(procurementCode):
    sql = "select materialInfo.materialCode,materialInfo.materialName,materialInfo.materialType,materialInfo.unit,materialInfo.inventoryNum+m.sum,m.sum,materialInfo.inventoryNum,materialInfo.supplier from materialInfo,(select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) sum from procurement p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode) m where materialInfo.materialCode=m.materialCode;"%(procurementCode)
    try:
        cur.execute(sql)
        result = cur.fetchall()
        return result
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 取消采购
def delete_procurementByCode(procurementCode, entryClerk):
    try:
        # 更新materialInOut
        cur.execute("select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum),materialInfo.unit,materialInfo.price,materialInfo.supplier from procurement p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode;" % (procurementCode))
        result = cur.fetchall()
        for i in result:
            # documentNumber = uuid.uuid1()  # 使用uuid生成唯一代号
            documentNumber=datetime.now().strftime('%Y%m%d%H%M%S%f') # 使用时间戳生成唯一代号
            # documentNumber=documentNumber[0:16] # 使用时间戳生成唯一代号
            documentNumber = procurementCode + documentNumber[10:16]  # 使用时间戳生成唯一代号
            documentTime=datetime.now().strftime('%Y-%m-%d')
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            # insert_materialInOut(documentNumber, i[0], 0, i[1], i[2], i[3], i[4], entryTime, "系统账号")
            insert_materialInOut(documentNumber, documentTime, i[0], 0, i[1], i[2], i[3], i[4], entryTime, entryClerk)
        # 更新materialInfo
        cur.execute("update materialInfo,(select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) sum from procurement p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode) m set materialInfo.inventoryNum=materialInfo.inventoryNum+m.sum,materialInfo.inventoryMoney=materialInfo.inventoryMoney+price*m.sum where materialInfo.materialCode=m.materialCode;"%(procurementCode))
        # 执行SQL语句
        cur.execute("delete from procurement where procurementCode='%s';"%procurementCode)
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 插入采购表
def insert_procurement(procurementCode,productCodeArr,productNumArr,client,remarkArr,entryClerk,entryTime):
    try:
        for i in range(productCodeArr.__len__()):
            sql = "insert into procurement (procurementCode,productCode,productNum,client,remark,entryClerk,entryTime)value('%s','%s','%d','%s','%s','%s','%s');" \
                  % (procurementCode,productCodeArr[i],int(productNumArr[i]),client,remarkArr[i],entryClerk,entryTime)
            # 执行SQL语句
            cur.execute(sql)
        # 更新materialInOut
        cur.execute("select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum),materialInfo.unit,materialInfo.price,materialInfo.supplier from procurement p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode;" % (procurementCode))
        result = cur.fetchall()
        for i in result:
            # documentNumber=uuid.uuid1() # 使用uuid生成唯一代号
            documentNumber=datetime.now().strftime('%Y%m%d%H%M%S%f') # 使用时间戳生成唯一代号
            documentNumber=procurementCode+documentNumber[10:16] # 使用时间戳生成唯一代号
            documentTime=datetime.now().strftime('%Y-%m-%d')
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            # insert_materialInOut(documentNumber,i[0],1,i[1],i[2],i[3],i[4],entryTime,"系统账号")
            insert_materialInOut(documentNumber,documentTime,i[0],1,i[1],i[2],i[3],i[4],entryTime,entryClerk)
        # 更新materialInfo
        cur.execute("update materialInfo,(select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) sum from procurement p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode) m set materialInfo.inventoryNum=materialInfo.inventoryNum-m.sum,materialInfo.inventoryMoney=materialInfo.inventoryMoney-price*m.sum where materialInfo.materialCode=m.materialCode;"%(procurementCode))
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 未启用
# 更新采购：只修改产品数量，只在内部更新出入库
def update_procurement(procurementCode,productCodeArr,productNumArr,client,remarkArr,entryClerk,entryTime):
    try:
        # 查询旧materialInOut
        cur.execute("select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) from procurement p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode;" % (procurementCode))
        resultOld = cur.fetchall()
        # 查询materialInOut近似的操作时间
        cur.execute("select entryTime from procurement where procurementCode='%s';" % (procurementCode))
        entryDate = cur.fetchall()
        for i in range(productCodeArr.__len__()):
            sql = "update procurement set productNum='%d',client='%s',remark='%s',entryClerk='%s' where procurementCode='%s' and productCode='%s';" \
                  % (int(productNumArr[i]),client,remarkArr[i],entryClerk,procurementCode, productCodeArr[i])
            cur.execute(sql)
            sql = "update productInfo set productNum='%d' where productCode='%s';" \
                  % (int(productNumArr[i]), productCodeArr[i])
            cur.execute(sql)
        # 更新materialInOut
        cur.execute("select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) from procurement p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode;" % (procurementCode))
        result = cur.fetchall()
        for i in range(result.__len__()):
            update_materialInOutByCode(result[i][0], resultOld[i][1]-result[i][1], entryDate[0][0])
        # 更新materialInfo
        cur.execute("update materialInfo,(select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) sum from procurement p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode) m set materialInfo.inventoryNum=materialInfo.inventoryNum-m.sum,materialInfo.inventoryMoney=materialInfo.inventoryMoney-price*m.sum where materialInfo.materialCode=m.materialCode;"%(procurementCode))
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有物料
def select_all_materials():
    sql = "select materialCode,materialName,materialType,inventoryNum,unit,price,inventoryMoney,supplier,remark from materialInfo;"
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 查询物料余库存金额
def select_sum_materials():
    sql = "select round(sum(inventoryMoney),2) from materialInfo;"
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 根据物料编码查询物料信息
def select_materialInfoByCode(materialCode):
    conn=db.conn()
    cursor=conn.cursor()
    try:
        sql = "select materialName,materialType,unit,inventoryNum,price,inventoryMoney,remark,supplier from materialInfo where materialCode='%s';" % materialCode
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        return result
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 模糊查询物料信息
def select_materialInfoForOptions(filterStr):
    sql = "select materialCode,materialName,materialType from materialInfo where concat(materialCode,materialName,materialType) like '%%%s%%';"%(filterStr)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result
    return None
    conn.close()

# xijiawei
# 模糊查询物料信息
# def select_materialInfoByFilter(filterStr):
#     try:
#         # sql = "select materialCode,materialName,materialType from materialInfo where concat(materialCode,materialName,materialType) like '%%%s%%';"%(filterStr)
#         # cur.execute(sql)
#         cur.execute("select materialCode,materialCode from materialInfo where materialCode like '%%%s%%';" % (filterStr))
#         result = cur.fetchall()
#         if result:
#             return result
#         cur.execute("select materialCode,materialName from materialInfo where materialName like '%%%s%%';" % (filterStr))
#         result = cur.fetchall()
#         if result:
#             return result
#         cur.execute("select materialCode,materialType from materialInfo where materialType like '%%%s%%';" % (filterStr))
#         result = cur.fetchall()
#         if result:
#             return result
#         return None
#         conn.close()
#     # except:
#     #     conn.rollback()
#     except Exception as e:
#         print("数据库操作异常：",e)
#         conn.rollback()

# xijiawei
# 模糊查询物料信息
# def select_materialInfoByFilter(filterStr):
#     try:
#         # sql = "select materialCode,materialName,materialType from materialInfo where concat(materialCode,materialName,materialType) like '%%%s%%';"%(filterStr)
#         # cur.execute(sql)
#         cursor=db.query("select materialCode,materialCode from materialInfo where materialCode like '%%%s%%';" % (filterStr))
#         result = cursor.fetchall()
#         if result:
#             print(result[0][0])
#             return result
#         cursor = db.query("select materialCode,materialName from materialInfo where materialName like '%%%s%%';" % (filterStr))
#         result = cursor.fetchall()
#         if result:
#             print(result[0][0])
#             return result
#         cursor = db.query("select materialCode,materialType from materialInfo where materialType like '%%%s%%';" % (filterStr))
#         result = cursor.fetchall()
#         if result:
#             print(result[0][0])
#             return result
#         return None
#     # except:
#     #     conn.rollback()
#     except Exception as e:
#         print("数据库操作异常：",e)
#         conn.rollback()

# xijiawei
# 模糊查询物料信息
# def select_materialInfoByFilter(filterStr):
#     thread=threading.Thread(target=select_materialInfoByFilterThread,args=(filterStr))
#     try:
#         thread.start()
#     except Exception as e:
#         print("线程异常：",e)
#
# def select_materialInfoByFilterThread(filterStr):
#     conn=db.conn()
#     cursor=conn.cursor()
#     try:
#         # sql = "select materialCode,materialName,materialType from materialInfo where concat(materialCode,materialName,materialType) like '%%%s%%';"%(filterStr)
#         # cur.execute(sql)
#         cursor.execute("select materialCode,materialCode from materialInfo where materialCode like '%%%s%%';" % (filterStr))
#         result = cursor.fetchall()
#         if result:
#             print(result[0][0])
#             return result
#         cursor.execute("select materialCode,materialName from materialInfo where materialName like '%%%s%%';" % (filterStr))
#         result = cursor.fetchall()
#         if result:
#             print(result[0][0])
#             return result
#         cursor.execute("select materialCode,materialType from materialInfo where materialType like '%%%s%%';" % (filterStr))
#         result = cursor.fetchall()
#         if result:
#             print(result[0][0])
#             return result
#         return None
#     # except:
#     #     conn.rollback()
#     except Exception as e:
#         print("数据库操作异常：",e)
#         conn.rollback()

# xijiawei
# 模糊查询物料信息
def select_materialInfoByFilter(filterStr):
    conn=db.conn()
    cursor=conn.cursor()
    try:
        # sql = "select materialCode,materialName,materialType from materialInfo where concat(materialCode,materialName,materialType) like '%%%s%%';"%(filterStr)
        # cur.execute(sql)
        cursor.execute("select materialCode,materialCode from materialInfo where materialCode like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            conn.close()
            return result
        cursor.execute("select materialCode,materialName from materialInfo where materialName like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            conn.close()
            return result
        cursor.execute("select materialCode,materialType from materialInfo where materialType like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            conn.close()
            return result
        return None
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 添加或更新物料
def insertOrUpdate_materialInfo(materialCode, materialType, materialName, remark):
    # sql = "replace into materialInfo(materialCode, materialType, materialName, remark) value('%s','%s','%s','%s');" \
    #       % (materialCode, materialType, materialName, remark)
    try:
        cur.execute("select materialCode from materialInfo where materialCode='%s';"%materialCode)
        result = cur.fetchall()
        if not result:
            cur.execute("insert into materialInfo(materialCode, materialName, materialType, remark) value('%s','%s','%s','%s');"
                        % (materialCode, materialName, materialType, remark))
        else:
            cur.execute("update materialInfo set materialName='%s', materialType='%s', remark='%s' where materialCode='%s';"
                        % (materialName, materialType, remark,materialCode))
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 更新物料库存数量
def update_materialInfo(materialCode, materialName, materialType, operateNum, price,unit,supplier):
    sql = "update materialInfo set materialName='%s',materialType='%s',inventoryNum=inventoryNum+'%d',unit='%s',price='%f',inventoryMoney=inventoryMoney+'%d'*'%f',supplier='%s' where materialCode='%s';" \
          % (materialName, materialType, operateNum, unit, price, operateNum, price,supplier, materialCode)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 更新余库存金额
        cur.execute("update materialInfo set inventoryMoney=price*inventoryNum where materialCode='%s';" % (materialCode))
        # 更新成品费用
        cur.execute("update materialsOfProduct mOP,materialInfo m set materialPrice=m.price,materialCost=m.price*materialNum where mOP.materialCode='%s' and mOP.materialCode=m.materialCode;" % materialCode)
        cur.execute("update productInfo p, (select productCode,sum(materialCost+patchCost) sum from materialsOfProduct where productCode in (select distinct productCode from materialsOfProduct where materialCode='%s') group by productCode) mOP set price=(mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost+p.profit)*p.taxRate,totalCost=mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost,materialCost=mOP.sum where p.productCode=mOP.productCode;" % materialCode)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 删除物料
def delete_materialByCode(materialCode):
    sql = "delete from materialInfo where materialCode='%s';" \
          % (materialCode)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 查询每个物料的最近3条出入库记录
def select_all_materialInOut():
    try:
        # sql = "select materialInOut.materialCode,materialInfo.materialName,materialInfo.materialType,materialInOut.isInOrOut,materialInOut.beforeinventoryNum,materialInOut.operateNum,materialInOut.unit,materialInfo.price,materialInOut.operateNum*materialInfo.price,materialInOut.supplier,materialInOut.documentNumber,materialInOut.operateTime,materialInOut.operatorName from materialInOut left join materialInfo on materialInOut.materialCode=materialInfo.materialCode;"
        sql = "select m.materialCode,materialInfo.materialName,materialInfo.materialType,m.isInOrOut,m.beforeinventoryNum,m.operateNum,m.unit,m.price,round(m.operateNum*m.price,2),m.supplier,m.documentNumber,date_format(m.documentTime,'%Y-%m-%d'),date_format(m.operateTime,'%Y-%m-%d %H:%i:%s.%f'),m.operatorName from (select a.* from materialInOut a where 3>(select count(*) from materialInOut b where b.materialCode=a.materialCode and b.operateTime>a.operateTime)) m left join materialInfo on m.materialCode=materialInfo.materialCode order by m.materialCode,m.operateTime desc;"
        cur.execute(sql)
        result = cur.fetchall()
        return result
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询每个物料的最近3条出入库记录
def select_sum_materialInOut():
    try:
        # sql = "select materialInOut.materialCode,materialInfo.materialName,materialInfo.materialType,materialInOut.isInOrOut,materialInOut.beforeinventoryNum,materialInOut.operateNum,materialInOut.unit,materialInfo.price,materialInOut.operateNum*materialInfo.price,materialInOut.supplier,materialInOut.documentNumber,materialInOut.operateTime,materialInOut.operatorName from materialInOut left join materialInfo on materialInOut.materialCode=materialInfo.materialCode;"
        sql = "select isInOrOut,sum(operateNum),round(sum(operateNum*price),2) from materialInOut group by isInOrOut;"
        cur.execute(sql)
        result = cur.fetchall()
        return result
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 根据时间段查询物料出入库记录
def select_all_materialInOutFilterByDate(startDate,endDate):
    sql = "select materialInOut.materialCode,materialInfo.materialName,materialInfo.materialType,materialInOut.isInOrOut,materialInOut.beforeinventoryNum,materialInOut.operateNum,materialInOut.unit,materialInOut.price,round(materialInOut.operateNum*materialInOut.price,2),materialInOut.supplier,materialInOut.documentNumber,date_format(materialInOut.documentTime,'%%Y-%%m-%%d'),date_format(materialInOut.operateTime,'%%Y-%%m-%%d %%H:%%i:%%S.%%f'),materialInOut.operatorName from materialInOut, materialInfo where materialInOut.materialCode=materialInfo.materialCode and materialInOut.documentTime>='%s' and materialInOut.documentTime<='%s' order by materialInOut.materialCode,materialInOut.operateTime desc;"%(startDate,endDate)
    print(sql)
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 根据物料编码查询物料出入库记录
def select_materialInOutByCode(materialCode):
    sql = "select * from materialInOut where materialCode='%s';"%(materialCode)
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 插入物料出入库记录
def insert_materialInOut(documentNumber,documentTime,materialCode,isInOrOut,operateNum,unit,price,supplier,operateTime,operatorName):
    try:
        cur.execute("select inventoryNum from materialInfo where materialCode='%s';"%(materialCode))
        result = cur.fetchall()
        if result:
            sql = "insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplier,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" \
                  % (documentNumber, documentTime, materialCode, isInOrOut, result[0][0], operateNum, unit, price, supplier, operateTime,operatorName)
        else:
            sql = "insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplier,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" \
                  % (documentNumber, documentTime, materialCode, isInOrOut, 0, operateNum, unit, price, supplier, operateTime,operatorName)
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 更新物料出入库记录，更新相关物料出入库记录物料数量，并更新materialInfo表
def update_materialInOut(documentNumber, documentTime, isInOrOut, operateNum, unit, price, supplier, operateTime, operatorName, beforeInventoryNum):
    try:
        # cur.execute("select materialCode,isInOrOut,operateNum,operateTime from materialInOut where documentNumber='%s';" % (documentNumber))
        # result = cur.fetchall()
        # if result:
        #     materialCode=result[0][0]
        #     beforeIsInOrOut=result[0][1]
        #     beforeOperateNum=result[0][2]
        #     operateTime=result[0][3]
        #     if beforeIsInOrOut==0 and isInOrOut==0:
        #         cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % ((operateNum-beforeOperateNum),materialCode,operateTime))
        #         # 更新materialInfo表
        #         cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%d'*price where materialCode='%s';" % ((operateNum-beforeOperateNum), (operateNum-beforeOperateNum), materialCode))
        #     elif beforeIsInOrOut==1 and isInOrOut==0:
        #         cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % ((operateNum+beforeOperateNum),materialCode,operateTime))
        #         # 更新materialInfo表
        #         cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%d'*price where materialCode='%s';" % ((operateNum+beforeOperateNum), (operateNum+beforeOperateNum), materialCode))
        #     elif beforeIsInOrOut==0 and isInOrOut==1:
        #         cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum-'%d' where materialCode='%s' and operateTime>'%s';" % ((operateNum+beforeOperateNum),materialCode,operateTime))
        #         # 更新materialInfo表
        #         cur.execute("update materialInfo set inventoryNum=inventoryNum-'%d',inventoryMoney=inventoryMoney-'%d'*price where materialCode='%s';" % ((operateNum+beforeOperateNum), (operateNum+beforeOperateNum), materialCode))
        #     elif beforeIsInOrOut==1 and isInOrOut==1:
        #         cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum-'%d' where materialCode='%s' and operateTime>'%s';" % ((operateNum-beforeOperateNum),materialCode,operateTime))
        #         # 更新materialInfo表
        #         cur.execute("update materialInfo set inventoryNum=inventoryNum-'%d',inventoryMoney=inventoryMoney-'%d'*price where materialCode='%s';" % ((operateNum-beforeOperateNum), (operateNum-beforeOperateNum), materialCode))
        # sql = "update materialInOut set isInOrOut='%d',operateNum='%d',unit='%s',price='%f',supplier='%s' where documentNumber='%s';" \
        #           % (isInOrOut, operateNum, unit, price, supplier, documentNumber)
        # # 执行SQL语句
        # cur.execute(sql)

        cur.execute("select materialCode,isInOrOut,price,operateNum,operateTime from materialInOut where documentNumber='%s';" % (documentNumber))
        result = cur.fetchall()
        cur.execute("delete from materialInOut where documentNumber='%s';" % (documentNumber))
        if result:
            materialCode=result[0][0]
            beforeIsInOrOut=result[0][1]
            beforePrice=result[0][2]
            beforeOperateNum=result[0][3]
            beforeOperateTime=result[0][4]
            if beforeIsInOrOut==0 and isInOrOut==0:
                # 更新materialInOut表（相当于撤销此条出入库记录，调整为最新）
                cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % (-beforeOperateNum,materialCode,beforeOperateTime))
                # 更新materialInfo表
                cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%f',unit='%s',price='%f',supplier='%s' where materialCode='%s';" % ((operateNum-beforeOperateNum), (operateNum*price-beforeOperateNum*beforePrice), unit, price, supplier, materialCode))
                # 插入materialInOut表
                cur.execute("insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplier,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" % (documentNumber, documentTime, materialCode, isInOrOut, beforeInventoryNum-beforeOperateNum, operateNum, unit, price, supplier, operateTime, operatorName))
            elif beforeIsInOrOut==1 and isInOrOut==0:
                cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % (beforeOperateNum,materialCode,beforeOperateTime))
                # 更新materialInfo表
                cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%f',unit='%s',price='%f',supplier='%s' where materialCode='%s';" % ((operateNum+beforeOperateNum), (operateNum*price+beforeOperateNum*beforePrice), unit, price, supplier, materialCode))
                # 插入materialInOut表
                cur.execute("insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplier,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" % (documentNumber, documentTime, materialCode, isInOrOut, beforeInventoryNum+beforeOperateNum, operateNum, unit, price, supplier, operateTime, operatorName))
            elif beforeIsInOrOut==0 and isInOrOut==1:
                cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % (-beforeOperateNum,materialCode,beforeOperateTime))
                # 更新materialInfo表
                cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%f',unit='%s',price='%f',supplier='%s' where materialCode='%s';" % ((-operateNum-beforeOperateNum), (-operateNum*price-beforeOperateNum*beforePrice), unit, price, supplier, materialCode))
                # 插入materialInOut表
                cur.execute("insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplier,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" % (documentNumber, documentTime, materialCode, isInOrOut, beforeInventoryNum-beforeOperateNum, operateNum, unit, price, supplier, operateTime, operatorName))
            elif beforeIsInOrOut==1 and isInOrOut==1:
                cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % (beforeOperateNum,materialCode,beforeOperateTime))
                # 更新materialInfo表
                cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%f',unit='%s',price='%f',supplier='%s' where materialCode='%s';" % ((-operateNum+beforeOperateNum), (-operateNum*price+beforeOperateNum*beforePrice), unit, price, supplier, materialCode))
                # 插入materialInOut表
                cur.execute("insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplier,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" % (documentNumber, documentTime, materialCode, isInOrOut, beforeInventoryNum+beforeOperateNum, operateNum, unit, price, supplier, operateTime, operatorName))
            # 更新余库存金额
            cur.execute("update materialInfo set inventoryMoney=price*inventoryNum where materialCode='%s';" % (materialCode))
            # 更新成品费用
            cur.execute("update materialsOfProduct mOP,materialInfo m set materialPrice=m.price,materialCost=m.price*materialNum where mOP.materialCode='%s' and mOP.materialCode=m.materialCode;" % materialCode)
            cur.execute("update productInfo p, (select productCode,sum(materialCost+patchCost) sum from materialsOfProduct where productCode in (select distinct productCode from materialsOfProduct where materialCode='%s') group by productCode) mOP set price=(mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost+p.profit)*p.taxRate,totalCost=mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost,materialCost=mOP.sum where p.productCode=mOP.productCode;" % materialCode)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 更新物料出入库记录，更新相关物料出入库记录物料数量，并更新materialInfo表
def update_materialInOutByCode(materialCode, differenceOperateNum, operateTime):
    try:
        # 更新materialInOut表
        cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" %
                    (differenceOperateNum, materialCode, operateTime))
        # 更新materialInfo表
        cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%d'*price where materialCode='%s';" %
                    (differenceOperateNum, differenceOperateNum, materialCode))
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 根据单据号删除物料出入库记录，更新相关物料出入库记录物料数量，并更新materialInfo表
def delete_materialInOutByDocNum(documentNumber):
    try:
        cur.execute("select materialCode,isInOrOut,operateNum,operateTime from materialInOut where documentNumber='%s';" % (documentNumber))
        result = cur.fetchall()
        if result:
            materialCode = result[0][0]
            isInOrOut = result[0][1]
            operateNum = result[0][2]
            operateTime = result[0][3]
        if isInOrOut == 0:
            cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum-'%d' where materialCode='%s' and operateTime>'%s';" % (operateNum, materialCode, operateTime))
            # 更新materialInfo表
            cur.execute("update materialInfo set inventoryNum=inventoryNum-'%d',inventoryMoney=inventoryMoney-'%d'*price where materialCode='%s';" % (operateNum, operateNum, materialCode))
        if isInOrOut == 1:
            cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % (operateNum, materialCode, operateTime))
            # 更新materialInfo表
            cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%d'*price where materialCode='%s';" % (operateNum, operateNum, materialCode))
        # 更新materialInfo表price
        cur.execute(("select * from materialInOut a,(select materialCode,operateTime from materialInOut where documentNumber='%s') b where a.operateTime>b.operateTime and a.materialCode=b.materialCode;") % documentNumber)
        result = cur.fetchall()  # 如果记录为此物料最新记录，则查询结果为空
        if not result:
            cur.execute("delete from materialInOut where documentNumber='%s';" % (documentNumber))
            # cur.execute(("select materialCode,price from materialInOut,(select a.materialCode as mCode,max(a.operateTime) as latest from materialInOut a,(select materialCode from materialInOut where documentNumber='%s') b where a.materialCode=b.materialCode) m where materialCode=m.mCode and operateTime=m.latest;") % documentNumber)
            cur.execute(("select materialInOut.price from materialInOut,(select materialCode,max(operateTime) as latest from materialInOut where materialCode='%s') m where materialInOut.materialCode=m.materialCode and operateTime=m.latest;") % materialCode)
            price = cur.fetchall()
            if price:
                cur.execute("update materialInfo set price='%f' where materialCode='%s';" % (price[0][0], materialCode))
        else:
            cur.execute("delete from materialInOut where documentNumber='%s';" % (documentNumber))
        # 更新余库存金额
        cur.execute("update materialInfo set inventoryMoney=price*inventoryNum where materialCode='%s';" % (materialCode))
        # 更新成品费用
        cur.execute("update materialsOfProduct mOP,materialInfo m set materialPrice=m.price,materialCost=m.price*materialNum where mOP.materialCode='%s' and mOP.materialCode=m.materialCode;" % materialCode)
        cur.execute("update productInfo p, (select productCode,sum(materialCost+patchCost) sum from materialsOfProduct where productCode in (select distinct productCode from materialsOfProduct where materialCode='%s') group by productCode) mOP set price=(mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost+p.profit)*p.taxRate,totalCost=mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost,materialCost=mOP.sum where p.productCode=mOP.productCode;" % materialCode)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()
