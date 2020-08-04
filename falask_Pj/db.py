import threading
import pymysql

import uuid
from datetime import datetime

# 说明：
# 其中一些方法是可用不用、暂不用、弃用，分别表示：
# 可用不用：此方法是好方法，但是目前有更好的方法替代；
# 暂不用：此方法是备用的方法，目前业务逻辑暂未使用到此方法；
# 弃用：此方法是不好的方法，本身存在问题，作为错误示范

# 同步锁
lock=threading.Lock()

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="test", charset="utf8")
cur = conn.cursor()

# 多线程mysql（暂不用）
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

# 多线程mysql
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

        # if self.target(*self.args):
        #     self.result = self.target(*self.args)

        # result=self.target(*self.args)
        # if result:
        #     self.result = result

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
    lock.acquire()
    cur.execute(sql)
    result = cur.fetchall()
    lock.release()
    return result
    conn.close()

# xijiawei
# 管理员_人员管理_查看人员
def select_all_users_for_selector():
    sql = "select userid,username from users;"
    # print(sql)
    lock.acquire()
    cur.execute(sql)
    result = cur.fetchall()
    lock.release()
    return result
    conn.close()

# xijiawei
def select_user(username):
    sql = "select * from users where username='%s';"%username
    # print(sql)
    lock.acquire()
    cur.execute(sql)
    result = cur.fetchall()
    lock.release()
    return result
    conn.close()

# xijiawei
def login_check(username,password):
    sql = "select * from users where username='%s' and password='%s';"%(username,password)
    # print(sql)
    lock.acquire()
    cur.execute(sql)
    result = cur.fetchall()
    lock.release()
    if result:
        return result[0][0]
    else:
        return None
    conn.close()

# xijiawei
def select_user_password(username):
    sql = "select password from users where username='%s';"%username
    # print(sql)
    lock.acquire()
    cur.execute(sql)
    result = cur.fetchall()
    lock.release()
    if result:
        return result[0][0]
    else:
        return None
    conn.close()

# xijiawei
def select_user_authority(username):
    sql = "select authority from users where username='%s';"%username
    # print(sql)
    lock.acquire()
    cur.execute(sql)
    result = cur.fetchall()
    lock.release()
    if result:
        return result[0][0]
    else:
        return None
    conn.close()

# xijiawei
def insert_user(username, password, authority):
    sql = "insert into users (username, password, authority) value('%s','%s','%s');" % (username, password, authority)
    try:
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
        conn.close()
    except Exception as e:
        print("插入异常：", e)
        conn.rollback()

# xijiawei
# 展示所有成品
def select_all_products():
    sql = "select productCode,productType,client,price,profit,totalCost,remark,date_format(entryTime,'%Y-%m-%d %H:%i:%s.%f'),entryClerk from productInfo;"
    lock.acquire()
    cur.execute(sql)
    result = cur.fetchall()
    lock.release()
    return result
    conn.close()

# xijiawei
# 根据成品编码查询成品录入信息
def select_productChangeByCode(productCode):
    sql = "select entryClerk,updateOfContent,isUpdateOrAdd,entryTime from productChange where productCode='%s';" % (productCode)
    lock.acquire()
    cur.execute(sql)
    result = cur.fetchall()
    lock.release()
    return result
    conn.close()

# xijiawei
# 根据成品编码查询成品信息
def select_productInfoByCode(productCode):
    conn = db.conn()
    cursor = conn.cursor()
    try:
        sql = "select productType,client,uint,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk from productInfo where productCode='%s';" % (
            productCode)
        lock.acquire()
        cursor.execute(sql)
        result = cursor.fetchall()
        lock.release()
        conn.close()
        return result
    except Exception as e:
        print("异常：",e)
        conn.rollback()
        conn.close()

# xijiawei
# 根据成品编码查询成品信息
def select_productInfoByType(productType):
    conn = db.conn()
    cursor = conn.cursor()
    try:
        sql = "select productCode,client,uint,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk from productInfo where productType='%s';" % (productType)
        lock.acquire()
        cursor.execute(sql)
        result = cursor.fetchall()
        lock.release()
        conn.close()
        return result
    except Exception as e:
        print("异常：",e)
        conn.rollback()
        conn.close()

# xijiawei
# 根据成品编码查询成品物料组成
def select_materialsOfProductByCode(productCode):
    conn = db.conn()
    cursor = conn.cursor()
    try:
        sql = "select mOP.materialCode,m.materialName,m.materialType,mOP.materialNum,mOP.materialPrice,mOP.materialCost,mOP.patchPoint,mOP.patchPrice,mOP.patchCost from materialsOfProduct mOP,materialInfo m where productCode='%s' and mOP.materialCode=m.materialCode;" % (
            productCode)
        lock.acquire()
        cursor.execute(sql)
        result = cursor.fetchall()
        lock.release()
        conn.close()
        return result
    except Exception as e:
        print("异常：",e)
        conn.close()
        conn.rollback()

# xijiawei
# 根据多个成品编码汇总物料
def select_materialsOfProductByCodeArr(productCodeArr):
    conn = db.conn()
    cursor = conn.cursor()
    try:
        length = len(productCodeArr)
        if length == 0:
            return
        else:
            # sql="select m.materialCode,materialInfo.materialName,materialInfo.unit,materialInfo.inventoryNum,m.sum,materialInfo.inventoryNum-m.sum,materialInfo.supplierCode from (select materialInfo.materialCode,sum(materialsOfProduct.materialNum) sum from materialsOfProduct left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where materialsOfProduct.productCode='%s'"%productCodeArr[0]
            sql = "select m.materialCode,materialInfo.materialName,materialInfo.materialType,materialInfo.unit,materialInfo.inventoryNum,cast(m.sum as signed integer),cast(materialInfo.inventoryNum-m.sum as signed integer),materialInfo.supplierCode from (select materialInfo.materialCode,sum(materialsOfProduct.materialNum*productInfo.productNum) sum from materialsOfProduct left join productInfo on materialsOfProduct.productCode=productInfo.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where materialsOfProduct.productCode='%s'" % \
                  productCodeArr[0]
            for productCode in productCodeArr[1:productCodeArr.__len__()]:
                sql += " or materialsOfProduct.productCode='%s'" % productCode
            sql += " group by materialInfo.materialCode) m,materialInfo where materialInfo.materialCode=m.materialCode;"
            print(sql)
        lock.acquire()
        cursor.execute(sql)
        result = cursor.fetchall()
        lock.release()
        conn.close()
        return result
    except Exception as e:
        print("删除异常：",e)
        conn.rollback()
        conn.close()

# xijiawei
# 根据成品型号查询成品编码
def select_productCodeByType(productType):
    conn = db.conn()
    cursor = conn.cursor()
    try:
        sql = "select productCode from productInfo where productType='%s';" % (productType)
        lock.acquire()
        cursor.execute(sql)
        result = cursor.fetchall()
        lock.release()
        conn.close()
        return result
    except Exception as e:
        print("异常：",e)
        conn.rollback()
        conn.close()
        #lock.release()
    finally:
        print("查询编码")

# xijiawei
# 根据成品编码查询成品型号
def select_productTypeByCode(productCode):
    conn = db.conn()
    cursor = conn.cursor()
    try:
        sql = "select productType from productInfo where productCode='%s';" % (productCode)
        lock.acquire()
        cursor.execute(sql)
        result = cursor.fetchall()
        lock.release()
        conn.close()
        return result
    except Exception as e:
        print("异常：",e)
        conn.rollback()
        conn.close()
        #lock.release()
    finally:
        print("查询型号")

# xijiawei
# 根据成品编码查询成品其他成本组成信息
def select_otherCostsByCode(productCode):
    try:
        sql = "select processCost,adminstrationCost,supplementaryCost,operationCost,process, adminstration, supplementary, operation from otherCosts where productCode='%s';" % (
            productCode)
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
    except:
        conn.rollback()

# xijiawei
# 插入成品
def insert_productInfo(productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk):
    sql = "insert into productInfo (productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk)value('%s','%s','%s','%f','%f','%f','%f','%f','%f','%f','%f','%f','%s','%s','%s');" \
          % (productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk)
    try:
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 更新成品静态表的productNum字段
def update_productNumOfProductInfo(productCode,productNum):
    conn = db.conn()
    cursor = conn.cursor()
    try:
        sql = "update productInfo set productNum='%d' where productCode='%s';" % (productNum,productCode)
        lock.acquire()
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
        conn.close()
        print("语句已经提交")
        return True
    except:
        conn.rollback()
        conn.close()

# xijiawei
# 插入成品物料组成
def insert_materialsOfProduct(productCode,materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost):
    sql = "insert into materialsOfProduct (productCode,materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost) value('%s','%s','%d','%f','%f','%d','%f','%f');" \
          % (productCode,materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost)
    try:
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
    sql = "insert into productChange (productCode,entryClerk,updateOfContent,entryTime) value('%s','%s','%s','%s');" \
          % (productCode,entryClerk,updateOfContent,entryDate)
    try:
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("插入异常：", e)
        conn.rollback()

# xijiawei
# 更新成品
def update_productInfo(productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk):
    sql = "update productInfo set productType='%s',client='%s',price='%f',profit='%f',totalCost='%f',taxRate='%f',materialCost='%f',processCost='%f',adminstrationCost='%f',supplementaryCost='%f',operatingCost='%f',remark='%s',entryTime='%s',entryClerk='%s' where productCode='%s';" \
          % (productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk,productCode)
    try:
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 删除成品
def copy_productInfo(productCode, newProductCode, newProductType):
    try:
        lock.acquire()
        # 执行SQL语句
        cur.execute("insert into productInfo (productCode, productType, client, price, profit, totalCost, taxRate, materialCost, adminstrationCost, processCost, supplementaryCost, operatingCost, remark, entryTime, entryClerk) select '%s' as productCode, '%s' as productType, client, 0 as price, 0 as profit, 0 as totalCost, 1 as taxRate, materialCost, 0 as adminstrationCost, 0 as processCost, 0 as supplementaryCost, 0 as operatingCost, remark, entryTime, entryClerk from productInfo where productCode='%s'"%(newProductCode,newProductType,productCode))
        cur.execute("insert into materialsOfProduct (productCode, materialCode, materialNum, materialPrice, materialCost, patchPoint, patchPrice, patchCost, remark) select '%s' as productCode, materialCode, materialNum, materialPrice, materialCost, patchPoint, patchPrice, patchCost, remark from materialsOfProduct where productCode='%s';"% (newProductCode,productCode))
        cur.execute("update productInfo set totalCost=materialCost where productCode='%s';"%newProductCode)
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("删除异常：",e)
        conn.rollback()

# xijiawei
# 删除成品
def delete_productInfo(productCode):
    sql = "delete from productInfo where productCode='%s';" \
          % (productCode)
    try:
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
    # sql = "select id,group_concat(productCode),group_concat(productType),group_concat(productNum),group_concat(client),group_concat(entryClerk),group_concat(entryDate) from procurementInfo group by id;"
    sql = "select p2.count,p1.* from (select p.*,productInfo.productType,procurementInfo.productNum,procurementInfo.client,procurementInfo.entryClerk,procurementInfo.entryTime from (select t.*,group_concat(materialsOfProduct.materialCode),group_concat(materialInfo.materialName),group_concat(materialsOfProduct.materialNum) from (select procurementInfo.procurementCode,procurementInfo.productCode from procurementInfo left join productInfo on procurementInfo.productCode=productInfo.productCode) t left join materialsOfProduct on t.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode group by t.procurementCode,t.productCode) p,procurementInfo,productInfo where p.procurementCode=procurementInfo.procurementCode and p.productCode=procurementInfo.productCode and p.productCode=productInfo.productCode order by procurementInfo.entryTime) p1 left join (select count(procurementCode) count,procurementCode from procurementInfo group by procurementCode) p2 on p1.procurementCode=p2.procurementCode;"
    try:
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
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
    sql = "select p.productCode,productInfo.productType,p.productNum,p.client,p.remark,materialsOfProduct.materialCode,materialInfo.materialName,materialInfo.materialType,materialsOfProduct.materialNum from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s';"%(procurementCode)
    try:
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 根据采购代号汇总采购物料
# def select_materialsOfProcurementByCode(procurementCode):
#     sql = "select materialInfo.materialCode,materialInfo.materialName,materialInfo.materialType,materialInfo.unit,materialInfo.inventoryNum+m.sum,m.sum,materialInfo.inventoryNum,materialInfo.supplierCode from materialInfo,(select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) sum from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode) m where materialInfo.materialCode=m.materialCode;"%(procurementCode)
#     try:
#         lock.acquire()
#         cur.execute(sql)
#         result = cur.fetchall()
#         lock.release()
#         return result
#         conn.close()
#     except:
#         conn.rollback()

# xijiawei
# 根据采购代号查询采购
def select_materialsOfProcurementByCode(procurementCode):
    sql = "select p.materialCode,m.materialName,m.materialType,m.unit,p.beforeinventoryNum,p.materialNum,(p.beforeinventoryNum-p.materialNum),m.supplierCode from procurement p,materialInfo m where p.procurementCode='%s' and p.materialCode=m.materialCode;"%(procurementCode)
    try:
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 取消采购
def delete_procurementByCode(procurementCode, entryClerk):
    try:
        # 更新materialInOut
        # 方式一（弃用）：删除采购即原出库物料重新入库
        # lock.acquire()
        # cur.execute("select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum),materialInfo.unit,materialInfo.price,materialInfo.supplierCode from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode;" % (procurementCode))
        # result = cur.fetchall()
        # lock.release()
        # for i in result:
        #     # documentNumber = uuid.uuid1()  # 使用uuid生成唯一代号
        #     documentNumber=datetime.now().strftime('%Y%m%d%H%M%S%f') # 使用时间戳生成唯一代号
        #     # documentNumber=documentNumber[0:16] # 使用时间戳生成唯一代号
        #     print(documentNumber)
        #     print(documentNumber[12:20])
        #     documentNumber=procurementCode+documentNumber[12:20] # 使用时间戳生成唯一代号
        #     print(documentNumber)
        #     documentTime=datetime.now().strftime('%Y-%m-%d')
        #     entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        #     # insert_materialInOut(documentNumber, i[0], 0, i[1], i[2], i[3], i[4], entryTime, "系统账号")
        #     # insert_materialInOut(documentNumber, documentTime, i[0], 0, i[1], i[2], i[3], i[4], entryTime, entryClerk)
        #     myThread(target=insert_materialInOut, args=(documentNumber, documentTime, i[0], 0, i[1], i[2], i[3], i[4], entryTime, entryClerk, procurementCode,))
        # lock.acquire()
        # # 更新materialInfo
        # cur.execute("update materialInfo,(select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) sum from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode) m set materialInfo.inventoryNum=materialInfo.inventoryNum+m.sum,materialInfo.inventoryMoney=materialInfo.inventoryMoney+price*m.sum where materialInfo.materialCode=m.materialCode;"%(procurementCode))
        # 方式二：删除采购，删除对应的出库记录，并更新materialInOut其他记录
        cur.execute("select documentNumber from procurement where procurementCode='%s';" % procurementCode)
        result = cur.fetchall()
        for i in result:
            documentNumber = i[0]
            myThread(target=delete_materialInOutByDocNum, args=(documentNumber,))
        # 执行SQL语句
        cur.execute("delete from procurementInfo where procurementCode='%s';"%procurementCode)
        cur.execute("delete from procurement where procurementCode='%s';"%procurementCode)
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 插入采购表
def insert_procurement(procurementCode,productCodeArr,productNumArr,client,remarkArr,entryClerk,entryTime):
    try:
        lock.acquire()
        for i in range(productCodeArr.__len__()):
            sql = "insert into procurementInfo (procurementCode,productCode,productNum,client,remark,entryClerk,entryTime) value('%s','%s','%d','%s','%s','%s','%s');" \
                  % (procurementCode,productCodeArr[i],int(productNumArr[i]),client,remarkArr[i],entryClerk,entryTime)
            # 执行SQL语句
            cur.execute(sql)
        # 更新materialInOut
        cur.execute("select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum),materialInfo.unit,materialInfo.price,materialInfo.supplierCode from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode;" % (procurementCode))
        result = cur.fetchall()
        for i in result:
            # documentNumber=uuid.uuid1() # 使用uuid生成唯一代号
            documentNumber=datetime.now().strftime('%Y%m%d%H%M%S%f') # 使用时间戳生成唯一代号
            print(documentNumber)
            print(documentNumber[12:20])
            documentNumber=procurementCode+documentNumber[12:20] # 使用时间戳生成唯一代号
            print(documentNumber)

            cur.execute("select inventoryNum from materialInfo where materialCode='%s';" % (i[0]))
            inventoryNum = cur.fetchall()[0][0]
            cur.execute("insert into procurement (procurementCode, documentNumber, materialCode, beforeinventoryNum, materialNum) value('%s','%s','%s','%d','%d');" % (procurementCode,documentNumber,i[0],inventoryNum,i[1]))

            lock.release()
            documentTime=datetime.now().strftime('%Y-%m-%d')
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            # insert_materialInOut(documentNumber,i[0],1,i[1],i[2],i[3],i[4],entryTime,"系统账号")
            # insert_materialInOut(documentNumber,documentTime,i[0],1,i[1],i[2],i[3],i[4],entryTime,entryClerk)
            myThread(target=insert_materialInOut, args=(documentNumber, documentTime, i[0], 1, i[1], i[2], i[3], i[4], entryTime, entryClerk,))
            lock.acquire()
        # 更新materialInfo
        cur.execute("update materialInfo,(select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) sum from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode) m set materialInfo.inventoryNum=materialInfo.inventoryNum-m.sum,materialInfo.inventoryMoney=materialInfo.inventoryMoney-price*m.sum where materialInfo.materialCode=m.materialCode;"%(procurementCode))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 更新采购（弃用）：只修改产品数量，只在内部更新出入库
def update_procurement(procurementCode,productCodeArr,productNumArr,client,remarkArr,entryClerk,entryTime):
    try:
        lock.acquire()
        # 查询旧materialInOut
        cur.execute("select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode;" % (procurementCode))
        resultOld = cur.fetchall()
        # 查询materialInOut近似的操作时间
        cur.execute("select entryTime from procurementInfo where procurementCode='%s';" % (procurementCode))
        entryDate = cur.fetchall()
        for i in range(productCodeArr.__len__()):
            sql = "update procurementInfo set productNum='%d',client='%s',remark='%s',entryClerk='%s' where procurementCode='%s' and productCode='%s';" \
                  % (int(productNumArr[i]),client,remarkArr[i],entryClerk,procurementCode, productCodeArr[i])
            cur.execute(sql)
            sql = "update productInfo set productNum='%d' where productCode='%s';" \
                  % (int(productNumArr[i]), productCodeArr[i])
            cur.execute(sql)
        # 更新materialInOut
        cur.execute("select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode;" % (procurementCode))
        result = cur.fetchall()
        lock.release()
        for i in range(result.__len__()):
            # update_materialInOutByCode(result[i][0], resultOld[i][1]-result[i][1], entryDate[0][0])
            myThread(target=update_materialInOutByCode,args=(result[i][0], resultOld[i][1]-result[i][1], entryDate[0][0],))
        lock.acquire()
        # 更新materialInfo
        cur.execute("update materialInfo,(select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) sum from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode) m set materialInfo.inventoryNum=materialInfo.inventoryNum-m.sum,materialInfo.inventoryMoney=materialInfo.inventoryMoney-price*m.sum where materialInfo.materialCode=m.materialCode;"%(procurementCode))
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
    sql = "select materialCode,materialName,materialType,inventoryNum,unit,price,inventoryMoney,supplierCode,remark from materialInfo;"
    lock.acquire()
    cur.execute(sql)
    result=cur.fetchall()
    lock.release()
    return result
    conn.close()

# xijiawei
# 查询物料余库存金额
def select_sum_materials():
    sql = "select round(sum(inventoryMoney),2) from materialInfo;"
    lock.acquire()
    cur.execute(sql)
    result = cur.fetchall()
    lock.release()
    return result
    conn.close()

# xijiawei
# 根据物料编码查询物料信息
def select_materialInfoByCode(materialCode):
    conn=db.conn()
    cursor=conn.cursor()
    try:
        sql = "select materialName,materialType,unit,inventoryNum,price,inventoryMoney,remark,supplierCode from materialInfo where materialCode='%s';" % materialCode
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        return result
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()
        conn.close()

# xijiawei
# 模糊查询物料信息
def select_materialInfoForOptions(filterStr):
    sql = "select materialCode,materialName,materialType from materialInfo where concat(materialCode,materialName,materialType) like '%%%s%%';"%(filterStr)
    lock.acquire()
    cur.execute(sql)
    result = cur.fetchall()
    lock.release()
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
        conn.close()
        return None
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()
        conn.close()

# xijiawei
# 添加或更新物料
def insertOrUpdate_materialInfo(materialCode, materialType, materialName, remark):
    # sql = "replace into materialInfo(materialCode, materialType, materialName, remark) value('%s','%s','%s','%s');" \
    #       % (materialCode, materialType, materialName, remark)
    try:
        lock.acquire()
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
        lock.release()
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
def update_materialInfo(materialCode, materialName, materialType, operateNum, price,unit,supplierCode):
    sql = "update materialInfo set materialName='%s',materialType='%s',inventoryNum=inventoryNum+'%d',unit='%s',price='%f',inventoryMoney=inventoryMoney+'%d'*'%f',supplierCode='%s' where materialCode='%s';" \
          % (materialName, materialType, operateNum, unit, price, operateNum, price,supplierCode, materialCode)
    try:
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 更新余库存金额
        cur.execute("update materialInfo set inventoryMoney=price*inventoryNum where materialCode='%s';" % (materialCode))
        # 更新成品费用
        cur.execute("update materialsOfProduct mOP,materialInfo m set materialPrice=m.price,materialCost=m.price*materialNum where mOP.materialCode='%s' and mOP.materialCode=m.materialCode;" % materialCode)
        cur.execute("update productInfo p, (select productCode,sum(materialCost+patchCost) sum from materialsOfProduct where productCode in (select distinct productCode from materialsOfProduct where materialCode='%s') group by productCode) mOP set price=(mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost+p.profit)*p.taxRate,totalCost=mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost,materialCost=mOP.sum where p.productCode=mOP.productCode;" % materialCode)
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
        lock.acquire()
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 查询每个物料的最近3条出入库记录
def select_all_materialInOut():
    try:
        # sql = "select materialInOut.materialCode,materialInfo.materialName,materialInfo.materialType,materialInOut.isInOrOut,materialInOut.beforeinventoryNum,materialInOut.operateNum,materialInOut.unit,materialInfo.price,materialInOut.operateNum*materialInfo.price,materialInOut.supplierCode,materialInOut.documentNumber,materialInOut.operateTime,materialInOut.operatorName from materialInOut left join materialInfo on materialInOut.materialCode=materialInfo.materialCode;"
        sql = "select m.materialCode,materialInfo.materialName,materialInfo.materialType,m.isInOrOut,m.beforeinventoryNum,m.operateNum,m.unit,m.price,round(m.operateNum*m.price,2),m.supplierCode,m.documentNumber,date_format(m.documentTime,'%Y-%m-%d'),date_format(m.operateTime,'%Y-%m-%d %H:%i:%s.%f'),m.operatorName from (select a.* from materialInOut a where 3>(select count(*) from materialInOut b where b.materialCode=a.materialCode and b.operateTime>a.operateTime)) m left join materialInfo on m.materialCode=materialInfo.materialCode order by m.materialCode,m.operateTime desc;"
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询每个物料的最近3条出入库记录
def select_sum_materialInOut():
    try:
        # sql = "select materialInOut.materialCode,materialInfo.materialName,materialInfo.materialType,materialInOut.isInOrOut,materialInOut.beforeinventoryNum,materialInOut.operateNum,materialInOut.unit,materialInfo.price,materialInOut.operateNum*materialInfo.price,materialInOut.supplierCode,materialInOut.documentNumber,materialInOut.operateTime,materialInOut.operatorName from materialInOut left join materialInfo on materialInOut.materialCode=materialInfo.materialCode;"
        sql = "select isInOrOut,sum(operateNum),round(sum(operateNum*price),2) from materialInOut group by isInOrOut;"
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 根据时间段查询物料出入库记录
def select_all_materialInOutFilterByDate(startDate,endDate):
    sql = "select materialInOut.materialCode,materialInfo.materialName,materialInfo.materialType,materialInOut.isInOrOut,materialInOut.beforeinventoryNum,materialInOut.operateNum,materialInOut.unit,materialInOut.price,round(materialInOut.operateNum*materialInOut.price,2),materialInOut.supplierCode,materialInOut.documentNumber,date_format(materialInOut.documentTime,'%%Y-%%m-%%d'),date_format(materialInOut.operateTime,'%%Y-%%m-%%d %%H:%%i:%%S.%%f'),materialInOut.operatorName from materialInOut, materialInfo where materialInOut.materialCode=materialInfo.materialCode and materialInOut.documentTime>='%s' and materialInOut.documentTime<='%s' order by materialInOut.materialCode,materialInOut.operateTime desc;"%(startDate,endDate)
    print(sql)
    lock.acquire()
    cur.execute(sql)
    result = cur.fetchall()
    lock.release()
    return result
    conn.close()

# xijiawei
# 根据物料编码查询物料出入库记录
def select_materialInOutByCode(materialCode):
    sql = "select * from materialInOut where materialCode='%s';"%(materialCode)
    lock.acquire()
    cur.execute(sql)
    result = cur.fetchall()
    lock.release()
    return result
    conn.close()

# xijiawei
# 插入物料出入库记录
def insert_materialInOut(documentNumber,documentTime,materialCode,isInOrOut,operateNum,unit,price,supplierCode,operateTime,operatorName):
    try:
        lock.acquire()
        cur.execute("select inventoryNum from materialInfo where materialCode='%s';"%(materialCode))
        result = cur.fetchall()
        if result:
            beforeinventoryNum=result[0][0]
        else:
            beforeinventoryNum=0
        cur.execute("insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplierCode,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" % (documentNumber, documentTime, materialCode, isInOrOut, beforeinventoryNum, operateNum, unit, price, supplierCode, operateTime, operatorName))

        # 更新供应商的应付款，只关心入库操作
        if isInOrOut==0:
            payable = price * operateNum
            # 更新供应商
            cur.execute("select supplierCode from suppliers where supplierCode='%s';" % supplierCode)
            result = cur.fetchall()
            if result:
                cur.execute("update suppliers set payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s';" % (payable, operateTime, operatorName, supplierCode))
            else:
                cur.execute("insert into suppliers (supplierCode, supplier, payable, payment, entryTime, entryClerk) values ('%s','%s','%f','%f','%s','%s')" % (supplierCode, supplierCode, payable, 0, operateTime, operatorName))

            # 更新应付款报表
            month = documentTime[0:7]
            cur.execute("select supplierCode from payableReport where supplierCode='%s' and month='%s';" % (supplierCode, month))
            result = cur.fetchall()
            if result:
                cur.execute("update payableReport set addPayable=addPayable+'%f',payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month='%s';" % (payable, payable, operateTime, operatorName, supplierCode,month))
            else:
                cur.execute("select payable-payment from payableReport where supplierCode='%s' and month in (select max(month) from payableReport where supplierCode='%s' and month<'%s');" % (supplierCode, supplierCode, month))
                result = cur.fetchall()
                if result:
                    remainPayable = result[0][0]
                else:
                    remainPayable = 0
                cur.execute("insert into payableReport (supplierCode, month, remainPayable, addPayable, payable, payment, entryTime, entryClerk) value ('%s','%s','%f','%f','%f','%f','%s','%s');" % (supplierCode, month, remainPayable, payable, remainPayable + payable, 0, operateTime, operatorName))

            # 更新应付款明细报表
            cur.execute("select supplierCode from payableReportGroupByMaterialCode where supplierCode='%s' and materialCode='%s' and month='%s';" % (supplierCode, materialCode, month))
            result = cur.fetchall()
            if result:
                cur.execute("update payableReportGroupByMaterialCode set payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and materialCode='%s' and month='%s';" % (payable, operateTime, operatorName, supplierCode, materialCode, month))
            else:
                cur.execute("insert into payableReportGroupByMaterialCode (supplierCode, materialCode, month, payable, entryTime, entryClerk) value ('%s','%s','%s','%f','%s','%s');" % (supplierCode, materialCode, month, payable, operateTime, operatorName))

        # 执行SQL语句
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
def update_materialInOut(documentNumber, documentTime, isInOrOut, operateNum, unit, price, supplierCode, operateTime, operatorName, beforeInventoryNum):
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
        # sql = "update materialInOut set isInOrOut='%d',operateNum='%d',unit='%s',price='%f',supplierCode='%s' where documentNumber='%s';" \
        #           % (isInOrOut, operateNum, unit, price, supplierCode, documentNumber)
        # # 执行SQL语句
        # cur.execute(sql)

        lock.acquire()
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
                cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%f',unit='%s',price='%f',supplierCode='%s' where materialCode='%s';" % ((operateNum-beforeOperateNum), (operateNum*price-beforeOperateNum*beforePrice), unit, price, supplierCode, materialCode))
                # 插入materialInOut表
                cur.execute("insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplierCode,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" % (documentNumber, documentTime, materialCode, isInOrOut, beforeInventoryNum-beforeOperateNum, operateNum, unit, price, supplierCode, operateTime, operatorName))
            elif beforeIsInOrOut==1 and isInOrOut==0:
                cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % (beforeOperateNum,materialCode,beforeOperateTime))
                # 更新materialInfo表
                cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%f',unit='%s',price='%f',supplierCode='%s' where materialCode='%s';" % ((operateNum+beforeOperateNum), (operateNum*price+beforeOperateNum*beforePrice), unit, price, supplierCode, materialCode))
                # 插入materialInOut表
                cur.execute("insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplierCode,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" % (documentNumber, documentTime, materialCode, isInOrOut, beforeInventoryNum+beforeOperateNum, operateNum, unit, price, supplierCode, operateTime, operatorName))
            elif beforeIsInOrOut==0 and isInOrOut==1:
                cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % (-beforeOperateNum,materialCode,beforeOperateTime))
                # 更新materialInfo表
                cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%f',unit='%s',price='%f',supplierCode='%s' where materialCode='%s';" % ((-operateNum-beforeOperateNum), (-operateNum*price-beforeOperateNum*beforePrice), unit, price, supplierCode, materialCode))
                # 插入materialInOut表
                cur.execute("insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplierCode,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" % (documentNumber, documentTime, materialCode, isInOrOut, beforeInventoryNum-beforeOperateNum, operateNum, unit, price, supplierCode, operateTime, operatorName))
            elif beforeIsInOrOut==1 and isInOrOut==1:
                cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % (beforeOperateNum,materialCode,beforeOperateTime))
                # 更新materialInfo表
                cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%f',unit='%s',price='%f',supplierCode='%s' where materialCode='%s';" % ((-operateNum+beforeOperateNum), (-operateNum*price+beforeOperateNum*beforePrice), unit, price, supplierCode, materialCode))
                # 插入materialInOut表
                cur.execute("insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplierCode,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" % (documentNumber, documentTime, materialCode, isInOrOut, beforeInventoryNum+beforeOperateNum, operateNum, unit, price, supplierCode, operateTime, operatorName))
            # 更新余库存金额
            cur.execute("update materialInfo set inventoryMoney=price*inventoryNum where materialCode='%s';" % (materialCode))
            # 更新成品费用
            cur.execute("update materialsOfProduct mOP,materialInfo m set materialPrice=m.price,materialCost=m.price*materialNum where mOP.materialCode='%s' and mOP.materialCode=m.materialCode;" % materialCode)
            cur.execute("update productInfo p, (select productCode,sum(materialCost+patchCost) sum from materialsOfProduct where productCode in (select distinct productCode from materialsOfProduct where materialCode='%s') group by productCode) mOP set price=(mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost+p.profit)*p.taxRate,totalCost=mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost,materialCost=mOP.sum where p.productCode=mOP.productCode;" % materialCode)

            # 更新供应商的应付款，只关心入库操作
            if beforeIsInOrOut == 0 and isInOrOut == 0:
                payableDelta = operateNum*price-beforeOperateNum*beforePrice
            elif beforeIsInOrOut == 1 and isInOrOut == 0:
                payableDelta = operateNum*price
            elif beforeIsInOrOut == 0 and isInOrOut == 1:
                payableDelta = -beforeOperateNum*beforePrice
            month=documentTime[0:7]
            cur.execute("update suppliers set payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s';" % (payableDelta, operateTime, operatorName, supplierCode))
            cur.execute("update payableReport set addPayable=addPayable+'%f',payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month='%s';" % (payableDelta, payableDelta, operateTime, operatorName, supplierCode,month)) # 更新该月的addPayable
            cur.execute("update payableReport set remainPayable=remainPayable+'%f',payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month>'%s';" % (payableDelta, payableDelta, operateTime, operatorName, supplierCode,month)) # 更新该月以后月份的remainPayable
            cur.execute("update payableReportGroupByMaterialCode set payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and materialCode='%s' and month='%s';" % (payableDelta, operateTime, operatorName, supplierCode, materialCode, month))
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
        lock.acquire()
        # 更新materialInOut表
        cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" %
                    (differenceOperateNum, materialCode, operateTime))
        # 更新materialInfo表
        cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%d'*price where materialCode='%s';" %
                    (differenceOperateNum, differenceOperateNum, materialCode))
        # 提交到数据库执行
        conn.commit()
        lock.release()
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
        lock.acquire()
        cur.execute("select materialCode,isInOrOut,operateNum,operateTime,documentTime,supplierCode from materialInOut where documentNumber='%s';" % (documentNumber))
        result = cur.fetchall()
        if result:
            materialCode = result[0][0]
            isInOrOut = result[0][1]
            operateNum = result[0][2]
            operateTime = result[0][3]
            documentTime = result[0][4]
            supplierCode = result[0][5]
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

        # 更新供应商的应付款
        if isInOrOut == 0:
            payableDelta = -operateNum * price
            month = documentTime[0:7]
            cur.execute("update suppliers set payable=payable+'%f' where supplierCode='%s';" % (payableDelta, supplierCode))
            cur.execute("update payableReport set addPayable=addPayable+'%f',payable=payable+'%f' where supplierCode='%s' and month='%s';" % (payableDelta, payableDelta, supplierCode, month)) # 更新该月的addPayable
            cur.execute("update payableReport set remainPayable=remainPayable+'%f',payable=payable+'%f' where supplierCode='%s' and month>'%s';" % (payableDelta, payableDelta, supplierCode,month)) # 更新该月以后月份的remainPayable
            cur.execute("update payableReportGroupByMaterialCode set payable=payable+'%f' where supplierCode='%s' and materialCode='%s' and month='%s';" % (payableDelta, supplierCode, materialCode, month))

        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
        conn.close()
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

##### 订单 #####

# xijiawei
# 查询所有订单
def select_concated_orders():
    try:
        sql = "select orderCode, group_concat(distinct clientCode), group_concat(distinct orderDate), group_concat(productType), max(deliveryDate), (sum(deliveryNum)<=sum(deliveredNum)), group_concat(remark) from orders group by orderCode;"
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_orderByCode(orderCode):
    try:
        sql = "select client, address, contact, telephone, date_format(orderDate,'%%Y-%%m-%%d'), productType, deliveryNum, date_format(deliveryDate,'%%Y-%%m-%%d'), deliveredNum, uint, price, orders.receivable, orders.remark from orders,clients where orderCode='%s' and orders.clientCode=clients.clientCode;"%(orderCode)
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_orderByCodeAndType(orderCode,productType):
    try:
        lock.acquire()
        cur.execute("select deliveryNum-deliveredNum,inventoryNum from orders,productInfo where orderCode='%s' and orders.productType='%s' and orders.productType=productInfo.productType;" % (orderCode, productType))
        result = cur.fetchall()
        lock.release()
        return result
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_all_orderGroupByProductType():
    try:
        sql = "select clientCode, group_concat(productType), group_concat(remark) from orderGroupByProductType group by clientCode;"
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_all_orderGroupByProductTypeByCode(clientCode):
    try:
        sql = "select receivableReportGroupByProductType.productType,remainDeliveryNum,addDeliveryNum,deliveryNum,deliveredNum,inventoryNum,uint,price,receivable,receipt,receivableReportGroupByProductType.remark from receivableReportGroupByProductType,productInfo where clientCode='%s' and receivableReportGroupByProductType.productType=productInfo.productType;"%clientCode
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_orderGroupByProductTypeByCode(clientCode, productType):
    try:
        lock.acquire()
        cur.execute("select deliveryNum-deliveredNum,deliveredNum,p.inventoryNum from orderGroupByProductType orders, productInfo p where orders.clientCode='%s' and orders.productType='%s' and orders.productType=p.productType;" % (clientCode, productType))
        result = cur.fetchall()
        lock.release()
        return result
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def insert_order(orderCode, orderDate, clientCode, productType, deliveryNum, deliveryDate, uint, price, receivable, remark, entryTime, entryClerk):
    try:
        lock.acquire()
        cur.execute("insert into orders (orderCode, orderDate, clientCode, productType, deliveryNum, deliveryDate, deliveredNum, uint, price, receivable, remark, entryTime, entryClerk) values('%s','%s','%s','%s','%d','%s','%d','%s','%f','%f','%s','%s','%s');"%(orderCode, orderDate, clientCode, productType, deliveryNum, deliveryDate, 0, uint, price, receivable, remark, entryTime, entryClerk))

        # 更新交易客户的应收款
        cur.execute("select clientCode from clients where clientCode='%s';"%clientCode)
        result = cur.fetchall()
        if result:
            cur.execute("update clients set receivable=receivable+'%f', entryTime='%s', entryClerk='%s' where clientCode='%s';" % (receivable, entryTime, entryClerk, clientCode))
        else:
            cur.execute("insert into clients (clientCode, client, receivable, receipt, entryTime, entryClerk) values ('%s','%s','%f','%f','%s','%s')" % (clientCode, clientCode, receivable, 0, entryTime, entryClerk))

        # 更新订单报表
        month=orderDate[0:7]
        cur.execute("select clientCode from receivableReport where clientCode='%s' and month='%s';"%(clientCode,month))
        result = cur.fetchall()
        if result:
            cur.execute("update receivableReport set addReceivable=addReceivable+'%f',receivable=receivable+'%f', entryTime='%s', entryClerk='%s' where clientCode='%s' and month='%s';" % (receivable, receivable, entryTime, entryClerk, clientCode, month))
        else:
            # 方式一（可用不用）：要求每月都有报表数据
            # year_int = int(orderDate[0:4])
            # month_int = int(orderDate[5:7])
            # if month_int == 1:
            #     lastmonth = str(year_int - 1) + '-12'
            # else:
            #     lastmonth = orderDate[0:5] + str(month_int - 1)
            # cur.execute("select receivable-receipt from receivableReport where clientCode='%s' and month='%s';" % (clientCode, lastmonth))
            # result = cur.fetchall()
            # if result:
            #     remainReceivable=result[0][0]
            # else:
            #     remainReceivable=0
            # cur.execute("insert into receivableReport (clientCode, month, remainReceivable, addReceivable, receivable, receipt, remark, entryTime, entryClerk) value ('%s','%s','%f','%f','%f','%f','%s','%s','%s');" % (clientCode, month, remainReceivable+receivable, receivable, remainReceivable+receivable, 0, remark, entryTime, entryClerk))
            # 方式二：允许一些月份空数据
            cur.execute("select receivable-receipt from receivableReport where clientCode='%s' and month in (select max(month) from receivableReport where clientCode='%s' and month<'%s');" % (clientCode, clientCode, month))
            result = cur.fetchall()
            if result:
                remainReceivable = result[0][0]
            else:
                remainReceivable = 0
            cur.execute("insert into receivableReport (clientCode, month, remainReceivable, addReceivable, receivable, receipt, remark, entryTime, entryClerk) value ('%s','%s','%f','%f','%f','%f','%s','%s','%s');" % (clientCode, month, remainReceivable, receivable, remainReceivable + receivable, 0, remark, entryTime, entryClerk))

        # 更新orderGroupByProductType
        cur.execute("select clientCode from orderGroupByProductType where clientCode='%s' and productType='%s';"%(clientCode,productType))
        result = cur.fetchall()
        if result:
            cur.execute("update orderGroupByProductType set price='%f', deliveryNum=deliveryNum+'%f', receivable=receivable+'%f', remark=concat(remark,'%s'), entryTime='%s', entryClerk='%s' where clientCode='%s' and productType='%s';" % (price, deliveryNum, receivable, remark, entryTime, entryClerk, clientCode, productType))
        else:
            cur.execute("insert into orderGroupByProductType (clientCode, productType, uint, price, deliveryNum, deliveredNum, receivable, receipt, remark, entryTime, entryClerk) values ('%s','%s','%s','%f','%d','%d','%f','%f','%s','%s','%s');" % (clientCode, productType, uint, price, deliveryNum, 0, receivable, 0, remark, entryTime, entryClerk))

        # 更新receivableReportGroupByProductType
        cur.execute("select clientCode from receivableReportGroupByProductType where clientCode='%s' and productType='%s' and month='%s';"%(clientCode,productType,month))
        result = cur.fetchall()
        if result:
            cur.execute("update receivableReportGroupByProductType set addDeliveryNum=addDeliveryNum+'%d', deliveryNum=deliveryNum+'%d', addReceivable='%f', receivable=receivable+'%f', remark=concat(remark,'%s'), entryTime='%s', entryClerk='%s' where clientCode='%s' and productType='%s';" % (deliveryNum, deliveryNum, receivable, receivable, remark, entryTime, entryClerk, clientCode, productType))
        else:
            cur.execute("select deliveryNum-deliveredNum,receivable-receipt from receivableReportGroupByProductType where clientCode='%s' and month in (select max(month) from receivableReportGroupByProductType where clientCode='%s' and productType='%s' and month<'%s');" % (clientCode, clientCode, productType, month))
            result = cur.fetchall()
            if result:
                remainDeliveryNum = result[0][0]
                remainReceivable = result[0][1]
            else:
                remainDeliveryNum = 0
                remainReceivable = 0
            cur.execute("insert into receivableReportGroupByProductType (clientCode, productType, month, remainDeliveryNum, addDeliveryNum, deliveryNum, deliveredNum, remainReceivable, addReceivable, receivable, receipt, remark, entryTime, entryClerk) value ('%s','%s','%s','%d','%d','%d','%d','%f','%f','%f','%f','%s','%s','%s');" % (clientCode, productType, month, remainDeliveryNum, deliveryNum, deliveryNum, 0, remainReceivable, receivable, remainReceivable + receivable, 0, remark, entryTime, entryClerk))

        conn.commit()
        lock.release()
        return
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def update_order(orderCode, productType, sendNum, clientCode, client, contact, address, telephone):
    try:
        lock.acquire()
        cur.execute("update orders set deliveredNum=deliveredNum+'%d' where orderCode='%s' and productType='%s';"%(sendNum, orderCode, productType))
        cur.execute("update orderGroupByProductType set deliveredNum=deliveredNum+'%d' where clientCode='%s' and productType='%s';"%(sendNum, clientCode, productType))
        cur.execute("update clients set client='%s', contact='%s', address='%s', telephone='%s' where clientCode='%s';" % (client, contact, address, telephone, clientCode))
        conn.commit()
        lock.release()
        return
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def delete_order(orderCode):
    try:
        lock.acquire()
        cur.execute("update clients,(select group_concat(distinct clientCode) as cliCode,sum(receivable) as sumReceivable from orders where orderCode='%s' group by orderCode) as t set receivable=receivable-t.sumReceivable where clients.clientCode=t.cliCode;" % (orderCode))
        cur.execute("update receivableReport,(select group_concat(distinct clientCode) as cliCode, date_format(group_concat(distinct orderDate),'%%Y-%%m') as cliDate, sum(receivable) as sumReceivable from orders where orderCode='%s' group by orderCode) as t set addReceivable=addReceivable-t.sumReceivable,receivable=receivable-t.sumReceivable where receivableReport.clientCode=t.cliCode and receivableReport.month=t.cliDate;" % (orderCode)) # 更新该月的addReceivable
        cur.execute("update receivableReport,(select group_concat(distinct clientCode) as cliCode, date_format(group_concat(distinct orderDate),'%%Y-%%m') as cliDate, sum(receivable) as sumReceivable from orders where orderCode='%s' group by orderCode) as t set remainReceivable=remainReceivable-t.sumReceivable,receivable=receivable-t.sumReceivable where receivableReport.clientCode=t.cliCode and receivableReport.month>t.cliDate;" % (orderCode)) # 更新该月以后月份的remainReceivable
        cur.execute("update orderGroupByProductType,(select group_concat(distinct clientCode) as cliCode,group_concat(distinct productType) as prdType,sum(deliveryNum) as deliveryNumSum,sum(receivable) as receivableSum from orders where orderCode='%s' group by orderCode, productType) as t set deliveryNum=deliveryNum-t.deliveryNumSum,receivable=receivable-t.receivableSum where orderGroupByProductType.clientCode=t.cliCode and orderGroupByProductType.productType=t.prdType;" % (orderCode))
        cur.execute("update receivableReportGroupByProductType,(select group_concat(distinct clientCode) as cliCode,group_concat(distinct productType) as prdType, date_format(group_concat(distinct orderDate),'%%Y-%%m') as cliDate, sum(deliveryNum) as deliveryNumSum,sum(receivable) as receivableSum from orders where orderCode='%s' group by orderCode, productType) as t set addDeliveryNum=addDeliveryNum-t.deliveryNumSum,deliveryNum=deliveryNum-t.deliveryNumSum,addReceivable=addReceivable-t.receivableSum,receivable=receivable-t.receivableSum where clientCode=t.cliCode and productType=t.prdType and month=t.cliDate;" % (orderCode)) # 更新该月的addDeliveryNum和addReceivable
        cur.execute("update receivableReportGroupByProductType,(select group_concat(distinct clientCode) as cliCode,group_concat(distinct productType) as prdType, date_format(group_concat(distinct orderDate),'%%Y-%%m') as cliDate, sum(deliveryNum) as deliveryNumSum,sum(receivable) as receivableSum from orders where orderCode='%s' group by orderCode, productType) as t set remainDeliveryNum=remainDeliveryNum-t.deliveryNumSum,deliveryNum=deliveryNum-t.deliveryNumSum,remainReceivable=remainReceivable-t.receivableSum,receivable=receivable-t.receivableSum where clientCode=t.cliCode and productType=t.prdType and month>t.cliDate;" % (orderCode)) # 更新该月以后月份的remainDeliveryNum和remainReceivable
        cur.execute("delete from orders where orderCode='%s';"%(orderCode))
        conn.commit()
        lock.release()
        return
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

##### 出货 #####

# xijiawei
# 查询所有订单
def select_deliveryByCode(deliveryCode):
    try:
        sql = "select clients.client, clients.address, clients.contact, clients.telephone, orders.orderDate, orders.productType, deliveryNum, date_format(deliveryDate,'%%Y-%%m-%%d'), productInfo.uint, productInfo.price, date_format(sendDate,'%%Y-%%m-%%d'), sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, productInfo.inventoryNum, productInfo.inventoryNum-sendNum, delivery.remark, delivery.entryClerk from delivery,orders,clients,productInfo where deliveryCode='%s' and delivery.orderCode=orders.orderCode and delivery.productType=orders.productType and delivery.clientCode=clients.clientCode and delivery.productType=productInfo.productType;"%(deliveryCode)
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询某个订单的所有出货记录（暂不用）
def select_deliveryWithOrderByCode(orderCode):
    try:
        sql = "select orders.productType, orders.deliveryNum, date_format(deliveryDate,'%%Y-%%m-%%d'), deliveryCode, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, productInfo.inventoryNum,productInfo.inventoryNum-sendNum,delivery.remark, orders.clientCode, date_format(orderDate,'%Y-%m-%d') from orders,delivery,productInfo where orders.orderCode='%s' and orders.orderCode=delivery.orderCode and orders.productType=productInfo.productType;"%(orderCode)
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_deliveryByOrderCodeAndProductType(orderCode,productType):
    try:
        sql = "select deliveryCode, date_format(sendDate,'%%Y-%%m-%%d'), sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, productInfo.inventoryNum, productInfo.inventoryNum-sendNum, delivery.remark from delivery,productInfo where orderCode='%s' and delivery.productType='%s' and delivery.productType=productInfo.productType;"%(orderCode,productType)
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_deliveryGroupByProductTypeByCode(deliveryCode):
    try:
        sql = "select clients.client, clients.address, clients.contact, clients.telephone, date_format(d.sendDate,'%%Y-%%m-%%d'), d.productType, og.uint, og.price, sendNum, d.remark, d.entryClerk from deliveryGroupByProductType d,orderGroupByProductType og,clients where deliveryCode='%s' and d.clientCode=og.clientCode and d.productType=og.productType and d.clientCode=clients.clientCode;"%(deliveryCode)
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_deliveryGroupByProductTypeByClientCodeAndProductType(clientCode,productType):
    try:
        sql = "select deliveryCode, date_format(sendDate,'%%Y-%%m-%%d'), sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, remark from deliveryGroupByProductType where clientCode='%s' and productType='%s';"%(clientCode,productType)
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 插入订单出货
def insert_delivery(deliveryCode, orderCode, productType, beforeDeliveryNum, sendDate, sendNum, remark, clientCode, client, address, contact, telephone, entryTime, entryClerk):
    try:
        lock.acquire()
        cur.execute("insert into delivery (deliveryCode, orderCode, productType, beforeDeliveryNum, sendDate, sendNum, remark, clientCode, entryTime, entryClerk) values('%s','%s','%s','%d','%s','%d','%s','%s','%s','%s');"%(deliveryCode, orderCode, productType, beforeDeliveryNum, sendDate, sendNum, remark, clientCode, entryTime, entryClerk))
        conn.commit()
        lock.release()
        return
        conn.close()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 插入客户出货
def insert_deliveryGroupByProductType(deliveryCode, clientCode, productType, beforeDeliveryNum, sendDate, sendNum, remark, client, address, contact, telephone, entryTime, entryClerk):
    try:
        lock.acquire()
        cur.execute("insert into deliveryGroupByProductType (deliveryCode, clientCode, productType, beforeDeliveryNum, sendDate, sendNum, remark, entryTime, entryClerk) values('%s','%s','%s','%d','%s','%d','%s','%s','%s');"%(deliveryCode, clientCode, productType, beforeDeliveryNum, sendDate, sendNum, remark, entryTime, entryClerk))
        cur.execute("update clients set client='%s', contact='%s', address='%s', telephone='%s' where clientCode='%s';" % (client, contact, address, telephone, clientCode))
        cur.execute("update orderGroupByProductType set deliveredNum=deliveredNum+'%d' where clientCode='%s' and productType='%s';"%(sendNum,clientCode,productType))
        cur.execute("update receivableReportGroupByProductType set deliveredNum=deliveredNum+'%d' where clientCode='%s' and productType='%s' and month='%s';" % (sendNum, clientCode, productType,sendDate[0:7]))
        conn.commit()
        lock.release()
        return
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

##### 收款 #####

# xijiawei
# 查询所有订单
def select_all_clients():
    try:
        sql = "select clientCode, receivable, receipt, receivable-receipt from clients;"
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 模糊查询物料信息
def select_clientInfoByFilter(filterStr):
    conn=db.conn()
    cursor=conn.cursor()
    try:
        cursor.execute("select clientCode from clients where clientCode like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            conn.close()
            return result
        cursor.execute("select clientCode from clients where client like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            conn.close()
            return result
        conn.close()
        return None
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()
        conn.close()

# xijiawei
# 查询所有订单
def select_clientByCode(clientCode):
    try:
        sql = "select client, address, contact, telephone  from clients where clientCode='%s';"%clientCode
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_receiptsJournal(clientCode):
    try:
        sql = "select date_format(receiptDate,'%%Y-%%m-%%d'),beforeReceivable,receipt,remark from receiptsJournal where clientCode='%s';"%clientCode
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有客户应收款月度报表（暂不用）
def select_all_receivableReport(month):
    try:
        thread = myThread(target=select_all_clients, args=())
        clients = thread.get_result()
        result = []
        for i in clients:
            thread=myThread(target=select_receivableReportByCode, args=(i[0],month,))
            receivable=thread.get_result()
            result.append(receivable[0])
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_receivableReportByCode(clientCode,month):
    try:
        lock.acquire()
        cur.execute("select clientCode,remainReceivable,addReceivable,receivable,receipt,remark from receivableReport where clientCode='%s' and month='%s';" % (clientCode, month))
        result = cur.fetchall()
        if not result:
            cur.execute("select receivable-receipt from receivableReport where clientCode='%s' and month in (select max(month) from receivableReport where clientCode='%s' and month<'%s');" % (clientCode, clientCode, month))
            remainReceivableResult = cur.fetchall()
            if result:
                remainReceivable = remainReceivableResult[0][0]
            else:
                remainReceivable = 0
            result=[[clientCode,remainReceivable,0,remainReceivable,0,'']]
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_receivableReportGroupByProductTypeByCode(supplierCode,month):
    try:
        lock.acquire()
        cur.execute("select r.productType, r.addDeliveryNum, p.price, r.addReceivable, r.remark from receivableReportGroupByProductType r,productInfo p where clientCode='%s' and month='%s' and r.productType=p.productType;" % (supplierCode, month))
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def insert_receiptsJournal(clientCode,receiptDate,beforeReceivable,receipt,remark,entryTime,entryClerk):
    try:
        lock.acquire()
        cur.execute("insert into receiptsJournal (clientCode,receiptDate,beforeReceivable,receipt,remark,entryTime,entryClerk) values('%s','%s','%f','%f','%s','%s','%s');"%(clientCode,receiptDate,beforeReceivable,receipt,remark,entryTime,entryClerk))
        cur.execute("update clients set receipt=receipt+'%f', entryTime='%s', entryClerk='%s' where clientCode='%s';" % (receipt, entryTime, entryClerk, clientCode))
        cur.execute("update receivableReport set receipt=receipt+'%f', entryTime='%s', entryClerk='%s' where clientCode='%s' and month='%s';" % (receipt, entryTime, entryClerk, clientCode,receiptDate[0:7]))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

##### 付款 #####

# xijiawei
# 查询所有订单
def select_all_suppliers():
    try:
        sql = "select supplierCode,payable,payment,payable-payment from suppliers;"
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 模糊查询物料信息
def select_supplierInfoByFilter(filterStr):
    conn=db.conn()
    cursor=conn.cursor()
    try:
        cursor.execute("select supplierCode from suppliers where supplierCode like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            conn.close()
            return result
        cursor.execute("select supplierCode from suppliers where supplier like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            conn.close()
            return result
        conn.close()
        return None
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()
        conn.close()

# xijiawei
# 查询所有订单
def select_paymentsJournal(supplierCode):
    try:
        sql = "select date_format(paymentDate,'%%Y-%%m-%%d'),beforePayable,payment,remark from paymentsJournal where supplierCode='%s';"%supplierCode
        lock.acquire()
        cur.execute(sql)
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有供应商应付款月度报表（暂不用）
def select_all_payableReport(month):
    try:
        thread = myThread(target=select_all_suppliers, args=())
        suppliers = thread.get_result()
        result = []
        for i in suppliers:
            thread=myThread(target=select_payableReportByCode, args=(i[0],month,))
            payable=thread.get_result()
            result.append(payable[0])
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_payableReportByCode(supplierCode,month):
    try:
        lock.acquire()
        cur.execute("select supplierCode,remainPayable,addPayable,payable,payment,remark from payableReport where supplierCode='%s' and month='%s';" % (supplierCode, month))
        result = cur.fetchall()
        if not result:
            cur.execute("select payable-payment from payableReport where supplierCode='%s' and month in (select max(month) from payableReport where supplierCode='%s' and month<'%s');" % (supplierCode, supplierCode, month))
            remainPayableResult = cur.fetchall()
            if remainPayableResult:
                remainPayable = remainPayableResult[0][0]
            else:
                remainPayable = 0
            result=[[supplierCode,remainPayable,0,remainPayable,0,'']]
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_payableReportGroupByMaterialCodeByCode(supplierCode,month):
    try:
        lock.acquire()
        cur.execute("select materialCode,payable,remark from payableReportGroupByMaterialCode where supplierCode='%s' and month='%s';" % (supplierCode, month))
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def insert_paymentsJournal(supplierCode,paymentDate,beforePayable,payment,remark,entryTime,entryClerk):
    try:
        lock.acquire()
        cur.execute("insert into paymentsJournal (supplierCode,paymentDate,beforePayable,payment,remark,entryTime,entryClerk) values('%s','%s','%f','%f','%s','%s','%s');"%(supplierCode,paymentDate,beforePayable,payment,remark,entryTime,entryClerk))
        cur.execute("update suppliers set payment=payment+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s';" % (payment, entryTime, entryClerk, supplierCode))
        cur.execute("update payableReport set payment=payment+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month='%s';" % (payment, entryTime, entryClerk, supplierCode, paymentDate[0:7]))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

##### 工资 #####

# xijiawei
# 查询所有订单
def select_all_workerSalary():
    try:
        lock.acquire()
        cur.execute("select month, staff.staffid, name, position, workhours, overhours, timewage, piecewage, workagewage, subsidy, amerce, payablewage, tax, socialSecurityOfPersonal, otherdues, tax+socialSecurityOfPersonal+otherdues, realwage, socialSecurityOfEnterprise, salaryExpense  from staff,performance,workerSalary where staff.staffid=performance.staffid and staff.staffid=workerSalary.staffid order by staff.staffid;")
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def insert_workerSalary(month, name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk):
    try:
        lock.acquire()
        cur.execute("insert into staff (name, position, entryTime, entryClerk) values('%s','%s','%s','%s');" % (name, position, entryTime, entryClerk))
        cur.execute("select max(staffid) from staff;")
        staffid = cur.fetchall()[0][0]
        cur.execute("insert into performance (staffid, workhours, overhours, entryTime, entryClerk) values('%d','%d','%d','%s','%s');" % (staffid, workhours, overhours, entryTime, entryClerk))
        cur.execute("insert into workerSalary (staffid, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk) values('%d','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%s','%s');" % (staffid, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk))
        cur.execute("insert into workerSalaryRecord (month, staffid, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk) values('%s','%d','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%s','%s');" % (month, staffid, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk))
        conn.commit()
        lock.release()
        return staffid
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def update_workerSalary(month, staffid, name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk):
    try:
        lock.acquire()
        cur.execute("update staff set name='%s', position='%s', entryTime='%s', entryClerk='%s' where staffid='%d';" % (name, position, entryTime, entryClerk, staffid))
        cur.execute("update performance set workhours='%d', overhours='%d', entryTime='%s', entryClerk='%s' where staffid='%d';" % (workhours, overhours, entryTime, entryClerk, staffid))
        cur.execute("update workerSalary set month='%s', realwage='%f', aftertaxwage='%f', payablewage='%f', salaryExpense='%f', timewage='%f', piecewage='%f', workagewage='%f', subsidy='%f', amerce='%f', tax='%f', socialSecurityOfPersonal='%f', otherdues='%f', socialSecurityOfEnterprise='%f', entryTime='%s', entryClerk='%s' where staffid='%d';" % (month, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk, staffid))
        cur.execute("update workerSalaryRecord set realwage='%f', aftertaxwage='%f', payablewage='%f', salaryExpense='%f', timewage='%f', piecewage='%f', workagewage='%f', subsidy='%f', amerce='%f', tax='%f', socialSecurityOfPersonal='%f', otherdues='%f', socialSecurityOfEnterprise='%f', entryTime='%s', entryClerk='%s' where staffid='%d' and month='%s';" % (realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk, staffid, month))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def delete_staffByID(staffid):
    try:
        lock.acquire()
        cur.execute("delete from staff where staffid='%d';"%staffid)
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_all_managerSalary():
    try:
        lock.acquire()
        cur.execute("select month, staff.staffid, name, position, workhours, overhours, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, payablewage, tax, socialSecurityOfPersonal, otherdues, tax+socialSecurityOfPersonal+otherdues, realwage, socialSecurityOfEnterprise, salaryExpense  from staff,performance,managerSalary where staff.staffid=performance.staffid and staff.staffid=managerSalary.staffid order by staff.staffid;")
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def insert_managerSalary(month, name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk):
    try:
        lock.acquire()
        cur.execute("insert into staff (name, position, entryTime, entryClerk) values('%s','%s','%s','%s');" % (name, position, entryTime, entryClerk))
        cur.execute("select max(staffid) from staff;")
        staffid = cur.fetchall()[0][0]
        cur.execute("insert into performance (staffid, workhours, overhours, entryTime, entryClerk) values('%d','%d','%d','%s','%s');" % (staffid, workhours, overhours, entryTime, entryClerk))
        cur.execute("insert into managerSalary (staffid, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk) values('%d','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%s','%s');" % (staffid, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk))
        cur.execute("insert into managerSalaryRecord (month, staffid, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk) values('%s','%d','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%s','%s');" % (month, staffid, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk))
        conn.commit()
        lock.release()
        return staffid
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def update_managerSalary(month, staffid, name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk):
    try:
        lock.acquire()
        cur.execute("update staff set name='%s', position='%s', entryTime='%s', entryClerk='%s' where staffid='%d';" % (name, position, entryTime, entryClerk, staffid))
        cur.execute("update performance set workhours='%d', overhours='%d', entryTime='%s', entryClerk='%s' where staffid='%d';" % (workhours, overhours, entryTime, entryClerk, staffid))
        cur.execute("update managerSalary set month='%s', realwage='%f', aftertaxwage='%f', payablewage='%f', salaryExpense='%f', basewage='%f', jobwage='%f', overtimewage='%f', performancewage='%f', workagewage='%f', subsidy='%f', amerce='%f', tax='%f', socialSecurityOfPersonal='%f', otherdues='%f', socialSecurityOfEnterprise='%f', entryTime='%s', entryClerk='%s' where staffid='%d';" % (month, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk, staffid))
        cur.execute("update managerSalaryRecord set realwage='%f', aftertaxwage='%f', payablewage='%f', salaryExpense='%f', basewage='%f', jobwage='%f', overtimewage='%f', performancewage='%f', workagewage='%f', subsidy='%f', amerce='%f', tax='%f', socialSecurityOfPersonal='%f', otherdues='%f', socialSecurityOfEnterprise='%f', entryTime='%s', entryClerk='%s' where staffid='%d' and month='%s';" % (realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk, staffid, month))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_workerSalaryByMonth(month):
    try:
        lock.acquire()
        cur.execute("select month, staff.staffid, name, position, workhours, overhours, timewage, piecewage, workagewage, subsidy, amerce, payablewage, tax, socialSecurityOfPersonal, otherdues, tax+socialSecurityOfPersonal+otherdues, realwage, socialSecurityOfEnterprise, salaryExpense  from staff,performance,workerSalaryRecord where month='%s' and staff.staffid=performance.staffid and staff.staffid=workerSalaryRecord.staffid order by staff.staffid;"%month)
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_managerSalaryByMonth(month):
    try:
        lock.acquire()
        cur.execute("select month, staff.staffid, name, position, workhours, overhours, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, payablewage, tax, socialSecurityOfPersonal, otherdues, tax+socialSecurityOfPersonal+otherdues, realwage, socialSecurityOfEnterprise, salaryExpense  from staff,performance,managerSalaryRecord where month='%s' and staff.staffid=performance.staffid and staff.staffid=managerSalaryRecord.staffid order by staff.staffid;"%month)
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_workerSalarySumByMonth(month):
    try:
        lock.acquire()
        cur.execute("select round(sum(salaryExpense),2)  from workerSalaryRecord where month='%s';"%month)
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_managerSalarySumByMonth(month):
    try:
        lock.acquire()
        cur.execute("select round(sum(salaryExpense),2)  from managerSalaryRecord where month='%s';" % month)
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

##### 其他费用之辅料 #####

# xijiawei
# 查询所有订单
def select_supplementarySuppliers():
    try:
        lock.acquire()
        cur.execute("select supplierCode from supplementarySuppliers;")
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 模糊查询物料信息
def select_supplementarySupplierInfoByFilter(filterStr):
    conn=db.conn()
    cursor=conn.cursor()
    try:
        cursor.execute("select supplierCode from supplementarySuppliers where supplierCode like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            conn.close()
            return result
        cursor.execute("select supplierCode from supplementarySuppliers where supplier like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            conn.close()
            return result
        conn.close()
        return None
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()
        conn.close()

# xijiawei
# 查询所有订单
def select_supplementaryByCode(supplierCode):
    try:
        lock.acquire()
        cur.execute("select supplierCode,supplementaryCode,date_format(inDate,'%%Y-%%m-%%d'),inNum,price,remark from supplementary where supplierCode='%s' order by inDate;"%supplierCode)
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_supplementaryByCodeAndMonth(supplierCode,month):
    try:
        lock.acquire()
        cur.execute("select supplierCode,date_format(inDate,'%%Y-%%m-%%d'),supplementaryCode,inNum,price,remark from supplementary where supplierCode='%s' and date_format(inDate,'%%Y-%%m')='%s';" % (supplierCode, month))
        result = cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_supplementaryPayableReportByCode(supplierCode,month):
    try:
        lock.acquire()
        cur.execute("select supplierCode,round(remainPayable,2),round(addPayable,2),round(payable,2),round(payment,2),remark from supplementaryPayableReport where supplierCode='%s' and month='%s';" % (supplierCode, month))
        result = cur.fetchall()
        if not result:
            cur.execute("select round(payable-payment,2) from supplementaryPayableReport where supplierCode='%s' and month in (select max(month) from supplementaryPayableReport where supplierCode='%s' and month<'%s');" % (supplierCode, supplierCode, month))
            remainPayableResult = cur.fetchall()
            if remainPayableResult:
                remainPayable = remainPayableResult[0][0]
            else:
                remainPayable = 0
            result=[[supplierCode,remainPayable,0,remainPayable,0,'']]
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def insert_supplementary(supplierCode,supplementaryCode,inDate,inNum,price,remark,entryTime,entryClerk):
    try:
        lock.acquire()
        inCode = "SP" + datetime.now().strftime('%Y%m%d%H%M%S%f')[0:16]  # 使用时间戳生成唯一代号
        cur.execute("insert into supplementary (inCode, supplierCode,supplementaryCode,inDate,inNum,price,remark,entryTime,entryClerk) values('%s','%s','%s','%s','%d','%f','%s','%s','%s');"%(inCode, supplierCode,supplementaryCode,inDate,inNum,price,remark,entryTime,entryClerk))

        payable = price * inNum
        # 更新供应商的应付款
        cur.execute("select supplierCode from supplementarySuppliers where supplierCode='%s';" % supplierCode)
        result = cur.fetchall()
        if result:
            cur.execute("update supplementarySuppliers set payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s';" % (payable, entryTime, entryClerk, supplierCode))
        else:
            cur.execute(
                "insert into supplementarySuppliers (supplierCode, supplier, payable, payment, entryTime, entryClerk) values ('%s','%s','%f','%f','%s','%s');" % (supplierCode, supplierCode, payable, 0, entryTime, entryClerk))

        # 更新应付款报表
        month = inDate[0:7]
        cur.execute("select supplierCode from supplementaryPayableReport where supplierCode='%s' and month='%s';" % (supplierCode, month))
        result = cur.fetchall()
        if result:
            cur.execute("update supplementaryPayableReport set addPayable=addPayable+'%f',payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month='%s';" % (payable, payable, entryTime, entryClerk, supplierCode, month))
        else:
            cur.execute("select payable-payment from supplementaryPayableReport where supplierCode='%s' and month in (select max(month) from supplementaryPayableReport where supplierCode='%s' and month<'%s');" % (supplierCode, supplierCode, month))
            result = cur.fetchall()
            if result:
                remainPayable = result[0][0]
            else:
                remainPayable = 0
            cur.execute("insert into supplementaryPayableReport (supplierCode, month, remainPayable, addPayable, payable, payment, entryTime, entryClerk) value ('%s','%s','%f','%f','%f','%f','%s','%s');" % (supplierCode, month, remainPayable, payable, remainPayable + payable, 0, entryTime, entryClerk))

        # 更新应付款明细报表
        # cur.execute("select supplierCode from supplementaryPayableReportGroupByMaterialCode where supplierCode='%s' and materialCode='%s' and month='%s';" % (supplierCode, supplementaryCode, month))
        # result = cur.fetchall()
        # if result:
        #     cur.execute("update payableReportGroupByMaterialCode set payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and materialCode='%s' and month='%s';" % (payable, entryTime, entryClerk, supplierCode, supplementaryCode, month))
        # else:
        #     cur.execute("insert into payableReportGroupByMaterialCode (supplierCode, materialCode, month, payable, entryTime, entryClerk) value ('%s','%s','%s','%f','%s','%s');" % (supplierCode, supplementaryCode, month, payable, entryTime, entryClerk))

        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def delete_supplementaryByCode(inCode, entryTime, entryClerk):
    try:
        lock.acquire()
        # 更新供应商的应付款
        cur.execute("update supplementarySuppliers a,supplementary b set payable=payable-inNum*price, a.entryTime='%s', a.entryClerk='%s' where inCode='%s' and a.supplierCode=b.supplierCode;" % (entryTime, entryClerk, inCode))

        # 更新应付款报表
        month=entryTime[0:7]
        cur.execute("update supplementaryPayableReport a,supplementary b set addPayable=addPayable-inNum*price,payable=payable-inNum*price, entryTime='%s', entryClerk='%s' where inCode='%s' and a.supplierCode=b.supplierCode and month=date_format(b.inDate,'%%Y-%%m');" % (entryTime, entryClerk, inCode)) # 更新该月的addPayable
        cur.execute("update supplementaryPayableReport a,supplementary b set remainPayable=remainPayable-inNum*price,payable=payable-inNum*price, entryTime='%s', entryClerk='%s' where inCode='%s' and a.supplierCode=b.supplierCode and month>date_format(b.inDate,'%%Y-%%m');" % (entryTime, entryClerk, inCode)) # 更新该月以后月份的remainPayable

        # 删除
        cur.execute("delete from supplementary where inCode='%s';"%(inCode))

        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def delete_supplementaryBySupplierCode(supplierCode, entryTime, entryClerk):
    try:
        lock.acquire()
        # # 更新供应商的应付款
        # cur.execute("update supplementarySuppliers,(select sum(inNum*price) as payableSum from supplementary where supplierCode='%s') t set payable=payable-t.payableSum, a.entryTime='%s', a.entryClerk='%s' where supplierCode='%s';" % (supplierCode, entryTime, entryClerk, supplierCode))
        # # 更新应付款报表
        # month=entryTime[0:7]
        # cur.execute("update supplementaryPayableReport,(select sum(inNum*price) as payableSum from supplementary where supplierCode='%s') t set addPayable=addPayable-t.payableSum,payable=payable-t.payableSum, entryTime='%s', entryClerk='%s' where supplierCode='%s' and month='%s';" % (supplierCode, entryTime, entryClerk, supplierCode, month))
        # # 删除
        # cur.execute("delete from supplementary where supplierCode='%s';"%(supplierCode))

        cur.execute("select inCode from supplementary where supplierCode='%s';"%supplierCode)
        result = cur.fetchall()
        for i in result:
            myThread(target=delete_supplementaryByCode, args=(i[0], entryTime, entryClerk,))

        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def insert_supplementaryPayments(supplierCode, paymentDate, beforePayable, payment, remark, entryTime, entryClerk):
    try:
        lock.acquire()
        cur.execute("insert into supplementaryPaymentsJournal (supplierCode,paymentDate,beforePayable,payment,remark,entryTime,entryClerk) values('%s','%s','%f','%f','%s','%s','%s');" % (supplierCode, paymentDate, beforePayable, payment, remark, entryTime, entryClerk))
        cur.execute("update supplementarySuppliers set payment=payment+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s';" % (payment, entryTime, entryClerk, supplierCode))
        cur.execute("update supplementaryPayableReport set payment=payment+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month='%s';" % (payment, entryTime, entryClerk, supplierCode, paymentDate[0:7]))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

##### 其他费用之运营 #####

# xijiawei
# 查询所有运营费用（暂不用）
def select_all_operation():
    try:
        lock.acquire()
        cur.execute("select costCode, costDate, cost, remark, entryTime, entryClerk from operation;")
        result=cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_operationsByMonth(month):
    try:
        lock.acquire()
        cur.execute("select costCode, costDate, cost, remark, entryTime, entryClerk from operation where date_format(costDate,'%%Y-%%m')='%s' order by costCode;"%month)
        result=cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_operationSumByMonth(month):
    try:
        lock.acquire()
        cur.execute("select round(sum(cost),2) from operation where date_format(costDate,'%%Y-%%m')='%s';"%month)
        result=cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 插入运营费用
def insert_operation(costDate, cost, remark, entryTime, entryClerk):
    try:
        lock.acquire()
        costCode = "C" + datetime.now().strftime('%Y%m%d%H%M%S%f')[0:16]  # 使用时间戳生成唯一代号
        cur.execute("insert into operation (costCode, costDate, cost, remark, entryTime, entryClerk) values('%s','%s','%f','%s','%s','%s');" % (costCode, costDate, cost, remark, entryTime, entryClerk))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 根据费用编号删除某项运营费用
def delete_operationByCode(costCode):
    try:
        lock.acquire()
        cur.execute("delete from operation where costCode='%s';" % (costCode))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 更新运营费用
def update_operation(costCode, costDate, cost, remark, entryTime, entryClerk):
    try:
        lock.acquire()
        cur.execute("update operation set costDate='%s', cost='%f', remark='%s', entryTime='%s', entryClerk='%s' where costCode='%s';" % (costDate, cost, remark, entryTime, entryClerk, costCode))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 删除某月所有运营费用（暂不用）
def delete_operationByMonth(month):
    try:
        lock.acquire()
        cur.execute("delete from operation where date_format(costDate,'%%Y-%%m')='%s';" % (month))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

##### 其他费用之售后 #####

# xijiawei
# 查询所有售后费用（暂不用）
def select_all_aftersale():
    try:
        lock.acquire()
        cur.execute("select costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk from aftersale;")
        result=cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_aftersalesByMonth(month):
    try:
        lock.acquire()
        cur.execute("select costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk from aftersale where date_format(costDate,'%%Y-%%m')='%s' order by costCode;"%month)
        result=cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_aftersaleSumByMonth(month):
    try:
        lock.acquire()
        cur.execute("select round(sum(laborCost),2), round(sum(materialCost),2), round(sum(otherCost),2) from aftersale where date_format(costDate,'%%Y-%%m')='%s';"%month)
        result=cur.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 插入售后费用
def insert_aftersale(costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk):
    try:
        lock.acquire()
        costCode = "C" + datetime.now().strftime('%Y%m%d%H%M%S%f')[0:16]  # 使用时间戳生成唯一代号
        cur.execute("insert into aftersale (costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk) values('%s','%s','%s','%s','%f','%f','%f','%s','%s','%s','%s');" % (costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 根据费用编号删除某项售后费用
def delete_aftersaleByCode(costCode):
    try:
        lock.acquire()
        cur.execute("delete from aftersale where costCode='%s';" % (costCode))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()

# xijiawei
# 更新售后费用
def update_aftersale(costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk):
    try:
        lock.acquire()
        cur.execute("update aftersale set costDate='%s', productType='%s', client='%s', laborCost='%f', materialCost='%f', otherCost='%f', trackNumber='%s', remark='%s', entryTime='%s', entryClerk='%s' where costCode='%s';" % (costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk, costCode))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        conn.rollback()
