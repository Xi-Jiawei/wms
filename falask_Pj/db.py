import threading
import pymysql

from datetime import datetime
from flask import current_app

# 说明：
# 其中一些方法是可用不用、暂不用、弃用，分别表示：
# 可用不用：此方法是好方法，但是目前有更好的方法替代；
# 暂不用：此方法是备用的方法，目前业务逻辑暂未使用到此方法；
# 弃用：此方法是不好的方法，本身存在问题，作为错误示范

# 同步锁
lock=threading.Lock()

# 单连接，不能保证长连接（暂不用）
# conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="test", charset="utf8", autocommit=True)

# 单连接，优化，能保证长连接
class mydb(object):
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="314159", db="test", charset="utf8", autocommit=True)

    def connect(self):
        try:
            self.conn.ping()
        except:
            self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="314159", db="test", charset="utf8", autocommit=True)
        return self.conn
db = mydb()

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

    def connect(self, ):
        name = threading.current_thread().name
        if name not in self.pool:
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset=self.charset)
            self.pool[name] = conn
        if self.pool[name]._closed:
            self.pool[name]=pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset=self.charset)
        return self.pool[name]
dbpool = dbHelper(host="127.0.0.1", port=3306, user="root", passwd="314159", db="test", charset="utf8")

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
    lock.acquire()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("select * from users;")
    result = cursor.fetchall()
    lock.release()
    return result

# xijiawei
# 管理员_人员管理_查看人员
def select_all_users_for_selector():
    lock.acquire()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("select userid,username from users;")
    result = cursor.fetchall()
    lock.release()
    return result

# xijiawei
def select_user(username):
    lock.acquire()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("select * from users where username='%s';" % username)
    result = cursor.fetchall()
    lock.release()
    return result

# xijiawei
def login_check(username,password):
    lock.acquire()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("select * from users where username='%s' and password='%s';" % (username, password))
    result = cursor.fetchall()
    lock.release()
    if result:
        return result[0][0]
    else:
        return None

# xijiawei
def select_user_password(username):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select password from users where username='%s';" % username)
        result = cursor.fetchall()
        lock.release()
        if result:
            return result[0][0]
        else:
            return None
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
def select_user_authority(username):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select authority from users where username='%s';" % username)
        result = cursor.fetchall()
        lock.release()
        if result:
            return result[0][0]
        else:
            return None
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
def insert_user(username, password, authority):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("insert into users (username, password, authority) value('%s','%s','%s');" % (username, password, authority))
        conn.commit()
        lock.release()
        return True
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
def update_user_authority(userid, authority):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("update users set authority='%s' where userid='%s';"% (authority, userid))
        conn.commit()
        lock.release()
        return True
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
def update_user_password(username, password):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("update users set password='%s' where username='%s';"% (password, username))
        conn.commit()
        lock.release()
        return True
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
def delete_userByID(userid):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("delete from users where userid='%s';" % userid)
        conn.commit()
        lock.release()
        return True
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 展示所有成品
def select_all_products():
    lock.acquire()
    conn = db.connect()
    cursor = conn.cursor()
    sql = "select productCode,productType,client,price,profit,totalCost,inventoryNum,remark,date_format(entryTime,'%Y-%m-%d %H:%i:%s.%f'),entryClerk from productInfo;"
    cursor.execute(sql)
    result = cursor.fetchall()
    lock.release()
    return result

# xijiawei
# 根据成品编码查询成品录入信息
def select_productChangeByCode(productCode):
    lock.acquire()
    conn = db.connect()
    cursor = conn.cursor()
    sql = "select entryClerk,updateOfContent,isUpdateOrAdd,entryTime from productChange where productCode='%s';" % (productCode)
    cursor.execute(sql)
    result = cursor.fetchall()
    lock.release()
    return result

# xijiawei
# 根据成品编码查询成品信息
def select_productInfoByCode(productCode):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        sql = "select productType,client,unit,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk from productInfo where productCode='%s';" % (productCode)
        lock.acquire()
        cursor.execute(sql)
        result = cursor.fetchall()
        lock.release()
        conn.close()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据成品编码查询成品信息
def select_productInfoByType(productType):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        sql = "select productCode,client,unit,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk from productInfo where productType='%s';" % (productType)
        lock.acquire()
        cursor.execute(sql)
        result = cursor.fetchall()
        lock.release()
        conn.close()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据成品编码查询成品物料组成
def select_materialsOfProductByCode(productCode):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        sql = "select mOP.materialCode,m.materialName,m.materialType,mOP.materialNum,mOP.materialPrice,mOP.materialCost,mOP.patchPoint,mOP.patchPrice,mOP.patchCost from materialsOfProduct mOP,materialInfo m where productCode='%s' and mOP.materialCode=m.materialCode;" % (productCode)
        lock.acquire()
        cursor.execute(sql)
        result = cursor.fetchall()
        lock.release()
        conn.close()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据多个成品编码汇总物料
def select_materialsOfProductByCodeArr(productCodeArr):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        length = len(productCodeArr)
        if length == 0:
            return
        else:
            # sql="select m.materialCode,materialInfo.materialName,materialInfo.unit,materialInfo.inventoryNum,m.sum,materialInfo.inventoryNum-m.sum,materialInfo.supplierCode from (select materialInfo.materialCode,sum(materialsOfProduct.materialNum) sum from materialsOfProduct left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where materialsOfProduct.productCode='%s'"%productCodeArr[0]
            sql = "select m.materialCode,materialInfo.materialName,materialInfo.materialType,materialInfo.unit,materialInfo.inventoryNum,cast(m.sum as signed integer),cast(materialInfo.inventoryNum-m.sum as signed integer),materialInfo.supplierCode from (select materialInfo.materialCode,sum(materialsOfProduct.materialNum*productInfo.productNum) sum from materialsOfProduct left join productInfo on materialsOfProduct.productCode=productInfo.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where materialsOfProduct.productCode='%s'" % productCodeArr[0]
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
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据成品型号查询成品编码
def select_productCodeByType(productType):
    conn = dbpool.connect()
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
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据成品编码查询成品型号
def select_productTypeByCode(productCode):
    conn = dbpool.connect()
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
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据成品编码查询成品其他成本组成信息
def select_otherCostsByCode(productCode):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        sql = "select processCost,adminstrationCost,supplementaryCost,operationCost,process, adminstration, supplementary, operation from otherCosts where productCode='%s';" % (productCode)
        lock.acquire()
        cursor.execute(sql)
        result = cursor.fetchall()
        lock.release()
        return result
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 模糊查询物料信息
def select_productInfoByFilter(filterStr):
    conn=dbpool.connect()
    cursor=conn.cursor()
    try:
        cursor.execute("select productType from productInfo where productCode like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            conn.close()
            return result
        cursor.execute("select productType from productInfo where productType like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            conn.close()
            return result
        conn.close()
        return None
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 插入成品
def insert_productInfo(productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute("insert into productInfo (productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk)value('%s','%s','%s','%f','%f','%f','%f','%f','%f','%f','%f','%f','%s','%s','%s');" % (productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 插入成品：部分修改权限
def insert_productInfoInPart(productCode,productType,client,totalCost,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute("insert into productInfo (productCode,productType,client,totalCost,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk)value('%s','%s','%s','%f','%f','%f','%f','%f','%f','%s','%s','%s');" % (productCode,productType,client,totalCost,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 更新成品静态表的productNum字段
def update_productNumOfProductInfo(productCode,productNum):
    conn = dbpool.connect()
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
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 插入成品物料组成
def insert_materialsOfProduct(productCode,materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute("insert into materialsOfProduct (productCode,materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost) value('%s','%s','%d','%f','%f','%d','%f','%f');" % (productCode,materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 插入成品其他成本组成
def insert_otherCosts(productCode,processCost,adminstrationCost,supplementaryCost,operationCost,process, adminstration, supplementary, operation):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute("insert into otherCosts (productCode,processCost,adminstrationCost,supplementaryCost,operationCost,process, adminstration, supplementary, operation) value('%s','%f','%f','%f','%f','%s','%s','%s','%s');" % (productCode,processCost,adminstrationCost,supplementaryCost,operationCost,process, adminstration, supplementary, operation))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 插入成品录入表
def insert_productChange(productCode,entryClerk,updateOfContent,entryDate):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute("insert into productChange (productCode,entryClerk,updateOfContent,entryTime) value('%s','%s','%s','%s');" % (productCode,entryClerk,updateOfContent,entryDate))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 更新成品
def update_productInfo(productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute("update productInfo set productType='%s',client='%s',price='%f',profit='%f',totalCost='%f',taxRate='%f',materialCost='%f',processCost='%f',adminstrationCost='%f',supplementaryCost='%f',operatingCost='%f',remark='%s',entryTime='%s',entryClerk='%s' where productCode='%s';" % (productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk,productCode))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 更新成品
def update_productInfoInPart(productCode,productType,client,totalCost,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute("update productInfo set productType='%s',client='%s',totalCost='%f',materialCost='%f',processCost='%f',adminstrationCost='%f',supplementaryCost='%f',operatingCost='%f',remark='%s',entryTime='%s',entryClerk='%s' where productCode='%s';" % (productType,client,totalCost,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,remark,entryTime,entryClerk,productCode))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 删除成品
def copy_productInfo(productCode, newProductCode, newProductType):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute("insert into productInfo (productCode, productType, client, price, profit, totalCost, taxRate, materialCost, adminstrationCost, processCost, supplementaryCost, operatingCost, remark, entryTime, entryClerk) select '%s' as productCode, '%s' as productType, client, 0 as price, 0 as profit, 0 as totalCost, 1 as taxRate, materialCost, 0 as adminstrationCost, 0 as processCost, 0 as supplementaryCost, 0 as operatingCost, remark, entryTime, entryClerk from productInfo where productCode='%s'"%(newProductCode,newProductType,productCode))
        cursor.execute("insert into materialsOfProduct (productCode, materialCode, materialNum, materialPrice, materialCost, patchPoint, patchPrice, patchCost, remark) select '%s' as productCode, materialCode, materialNum, materialPrice, materialCost, patchPoint, patchPrice, patchCost, remark from materialsOfProduct where productCode='%s';"% (newProductCode,productCode))
        cursor.execute("insert into otherCosts (productCode,processCost,adminstrationCost,supplementaryCost,operationCost,process,adminstration,supplementary,operation) select '%s' as productCode,processCost,adminstrationCost,supplementaryCost,operationCost,process,adminstration,supplementary,operation from otherCosts where productCode='%s';"% (newProductCode,productCode))
        cursor.execute("update productInfo set totalCost=materialCost where productCode='%s';"%newProductCode)
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 成品入库
def update_productInventoryNum(productCode, productNum, remark):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute("update productInfo set inventoryNum=inventoryNum+'%d' where productCode='%s';"%(productNum, productCode))
        # 提交到数据库执行
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 删除成品
def delete_productInfo(productCode):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute("delete from productInfo where productCode='%s';" % (productCode))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据成品编码更新成品物料组成
def update_materialsOfProduct(productCode,materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute("update materialsOfProduct set materialNum='%d',materialPrice='%f',materialCost='%f',patchPoint='%d',patchPrice='%f',patchCost='%f' where productCode='%s' and materialCode='%s';" % (materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost,productCode,materialCode))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    except:
        conn.rollback()

# xijiawei
# 根据成品编码删除成品物料组成
def delete_materialsOfProduct(productCode):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute("delete from materialsOfProduct where productCode='%s';" % (productCode))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据成品编码删除成品其他成本组成
def delete_otherCosts(productCode):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute("delete from otherCosts where productCode='%s';" % (productCode))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 检查物料组成表
def check_materialsOfProduct(productCode,materialCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        sql = "select * from materialsOfProduct where productCode= '%s' and materialCode='%s';" % (
        productCode, materialCode)
        cursor.execute(sql)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据成品编码检查成品表
def check_productInfoByCode(productCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        sql = "select * from productInfo where productCode= '%s';" % (productCode)
        cursor.execute(sql)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据成品型号检查成品表
def check_productInfoByType(productType):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        sql = "select * from productInfo where productType= '%s';" % (productType)
        cursor.execute(sql)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：", e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 检查物料表
def check_materialInfo(materialCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        sql = "select * from materialInfo where materialCode= '%s';" % (materialCode)
        cursor.execute(sql)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：", e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有采购
def select_procurement():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select p2.count,p1.* from (select p.*,productInfo.productType,procurementInfo.productNum,procurementInfo.client,procurementInfo.entryClerk,procurementInfo.entryTime from (select t.*,group_concat(materialsOfProduct.materialCode),group_concat(materialInfo.materialName),group_concat(materialsOfProduct.materialNum) from (select procurementInfo.procurementCode,procurementInfo.productCode from procurementInfo left join productInfo on procurementInfo.productCode=productInfo.productCode) t left join materialsOfProduct on t.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode group by t.procurementCode,t.productCode) p,procurementInfo,productInfo where p.procurementCode=procurementInfo.procurementCode and p.productCode=procurementInfo.productCode and p.productCode=productInfo.productCode order by procurementInfo.entryTime) p1 left join (select count(procurementCode) count,procurementCode from procurementInfo group by procurementCode) p2 on p1.procurementCode=p2.procurementCode;")
        result = cursor.fetchall()
        lock.release()
        return result
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据采购代号查询采购
def select_procurementByCode(procurementCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select p.productCode,productInfo.productType,p.productNum,p.client,p.remark,materialsOfProduct.materialCode,materialInfo.materialName,materialInfo.materialType,materialsOfProduct.materialNum from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s';" % (procurementCode))
        result = cursor.fetchall()
        lock.release()
        return result
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据采购代号汇总采购物料
# def select_materialsOfProcurementByCode(procurementCode):
#     sql = "select materialInfo.materialCode,materialInfo.materialName,materialInfo.materialType,materialInfo.unit,materialInfo.inventoryNum+m.sum,m.sum,materialInfo.inventoryNum,materialInfo.supplierCode from materialInfo,(select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) sum from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode) m where materialInfo.materialCode=m.materialCode;"%(procurementCode)
#     try:
#         lock.acquire()
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         lock.release()
#         return result
#         conn.close()
#     except:
#         conn.rollback()

# xijiawei
# 根据采购代号查询采购
def select_materialsOfProcurementByCode(procurementCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select p.materialCode,m.materialName,m.materialType,m.unit,p.beforeinventoryNum,p.materialNum,(p.beforeinventoryNum-p.materialNum),m.supplierCode from procurement p,materialInfo m where p.procurementCode='%s' and p.materialCode=m.materialCode;" % (procurementCode))
        result = cursor.fetchall()
        lock.release()
        return result
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 取消采购
def delete_procurementByCode(procurementCode, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        # 更新materialInOut
        # 方式一（弃用）：删除采购即原出库物料重新入库
        # lock.acquire()
        # cursor.execute("select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum),materialInfo.unit,materialInfo.price,materialInfo.supplierCode from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode;" % (procurementCode))
        # result = cursor.fetchall()
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
        # cursor.execute("update materialInfo,(select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) sum from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode) m set materialInfo.inventoryNum=materialInfo.inventoryNum+m.sum,materialInfo.inventoryMoney=materialInfo.inventoryMoney+price*m.sum where materialInfo.materialCode=m.materialCode;"%(procurementCode))
        # 方式二：删除采购，删除对应的出库记录，并更新materialInOut其他记录
        cursor.execute("select documentNumber from procurement where procurementCode='%s';" % procurementCode)
        result = cursor.fetchall()
        for i in result:
            documentNumber = i[0]
            myThread(target=delete_materialInOutByDocNum, args=(documentNumber,))
        # 执行SQL语句
        cursor.execute("delete from procurementInfo where procurementCode='%s';"%procurementCode)
        cursor.execute("delete from procurement where procurementCode='%s';"%procurementCode)
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 插入采购表
def insert_procurement(procurementCode,productCodeArr,productNumArr,client,remarkArr,entryClerk,entryTime):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        for i in range(productCodeArr.__len__()):
            sql = "insert into procurementInfo (procurementCode,productCode,productNum,client,remark,entryClerk,entryTime) value('%s','%s','%d','%s','%s','%s','%s');" \
                  % (procurementCode,productCodeArr[i],int(productNumArr[i]),client,remarkArr[i],entryClerk,entryTime)
            # 执行SQL语句
            cursor.execute(sql)
        # 更新materialInOut
        cursor.execute("select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum),materialInfo.unit,materialInfo.price,materialInfo.supplierCode from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode;" % (procurementCode))
        result = cursor.fetchall()
        documentNumber = datetime.now().strftime('%Y%m%d%H%M%S%f')  # 使用时间戳生成唯一代号
        documentNumber = int(documentNumber[0:16])  # 使用时间戳生成唯一代号
        for i in result:
            documentNumber+=1
            cursor.execute("select inventoryNum from materialInfo where materialCode='%s';" % (i[0]))
            inventoryNum = cursor.fetchall()[0][0]
            cursor.execute("insert into procurement (procurementCode, documentNumber, materialCode, beforeinventoryNum, materialNum) value('%s','%s','%s','%d','%d');" % (procurementCode,str(documentNumber),i[0],inventoryNum,i[1]))

            lock.release()
            documentTime=datetime.now().strftime('%Y-%m-%d')
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            # insert_materialInOut(documentNumber,i[0],1,i[1],i[2],i[3],i[4],entryTime,"系统账号")
            # insert_materialInOut(documentNumber,documentTime,i[0],1,i[1],i[2],i[3],i[4],entryTime,entryClerk)
            myThread(target=insert_materialInOut, args=(str(documentNumber), documentTime, i[0], 1, i[1], i[2], i[3], i[4], entryTime, entryClerk,))
            lock.acquire()
        # 更新materialInfo
        cursor.execute("update materialInfo,(select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) sum from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode) m set materialInfo.inventoryNum=materialInfo.inventoryNum-m.sum,materialInfo.inventoryMoney=materialInfo.inventoryMoney-price*m.sum where materialInfo.materialCode=m.materialCode;"%(procurementCode))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 更新采购（弃用）：只修改产品数量，只在内部更新出入库
def update_procurement(procurementCode,productCodeArr,productNumArr,client,remarkArr,entryClerk,entryTime):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 查询旧materialInOut
        cursor.execute("select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode;" % (procurementCode))
        resultOld = cursor.fetchall()
        # 查询materialInOut近似的操作时间
        cursor.execute("select entryTime from procurementInfo where procurementCode='%s';" % (procurementCode))
        entryDate = cursor.fetchall()
        for i in range(productCodeArr.__len__()):
            sql = "update procurementInfo set productNum='%d',client='%s',remark='%s',entryClerk='%s' where procurementCode='%s' and productCode='%s';" \
                  % (int(productNumArr[i]),client,remarkArr[i],entryClerk,procurementCode, productCodeArr[i])
            cursor.execute(sql)
            sql = "update productInfo set productNum='%d' where productCode='%s';" \
                  % (int(productNumArr[i]), productCodeArr[i])
            cursor.execute(sql)
        # 更新materialInOut
        cursor.execute("select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode;" % (procurementCode))
        result = cursor.fetchall()
        lock.release()
        for i in range(result.__len__()):
            # update_materialInOutByCode(result[i][0], resultOld[i][1]-result[i][1], entryDate[0][0])
            myThread(target=update_materialInOutByCode,args=(result[i][0], resultOld[i][1]-result[i][1], entryDate[0][0],))
        lock.acquire()
        # 更新materialInfo
        cursor.execute("update materialInfo,(select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) sum from procurementInfo p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode) m set materialInfo.inventoryNum=materialInfo.inventoryNum-m.sum,materialInfo.inventoryMoney=materialInfo.inventoryMoney-price*m.sum where materialInfo.materialCode=m.materialCode;"%(procurementCode))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有物料
def select_all_materials():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select materialCode,materialName,materialType,inventoryNum,unit,price,inventoryMoney,supplierCode,remark from materialInfo;")
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询物料余库存金额
def select_sum_materials():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select round(sum(inventoryMoney),2) from materialInfo;")
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据物料编码查询物料信息
def select_materialInfoByCode(materialCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select materialName,materialType,unit,inventoryNum,price,inventoryMoney,remark,supplierCode from materialInfo where materialCode='%s';" % materialCode)
        result = cursor.fetchall()
        lock.release()
        return result
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 模糊查询物料信息
def select_materialInfoForOptions(filterStr):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select materialCode,materialName,materialType from materialInfo where concat(materialCode,materialName,materialType) like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        lock.release()
        if result:
            return result
        return None
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 模糊查询物料信息
# def select_materialInfoByFilter(filterStr):
#     try:
#         # sql = "select materialCode,materialName,materialType from materialInfo where concat(materialCode,materialName,materialType) like '%%%s%%';"%(filterStr)
#         # cursor.execute(sql)
#         cursor.execute("select materialCode,materialCode from materialInfo where materialCode like '%%%s%%';" % (filterStr))
#         result = cursor.fetchall()
#         if result:
#             return result
#         cursor.execute("select materialCode,materialName from materialInfo where materialName like '%%%s%%';" % (filterStr))
#         result = cursor.fetchall()
#         if result:
#             return result
#         cursor.execute("select materialCode,materialType from materialInfo where materialType like '%%%s%%';" % (filterStr))
#         result = cursor.fetchall()
#         if result:
#             return result
#         return None
#         conn.close()
#     # except:
#     #     conn.rollback()
#     except Exception as e:
#         print("数据库操作异常：",e)
#         current_app.logger.exception(e)
#         conn.rollback()

# xijiawei
# 模糊查询物料信息
# def select_materialInfoByFilter(filterStr):
#     try:
#         # sql = "select materialCode,materialName,materialType from materialInfo where concat(materialCode,materialName,materialType) like '%%%s%%';"%(filterStr)
#         # cursor.execute(sql)
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
#         current_app.logger.exception(e)
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
#     conn=dbpool.connect()
#     cursor=conn.cursor()
#     try:
#         # sql = "select materialCode,materialName,materialType from materialInfo where concat(materialCode,materialName,materialType) like '%%%s%%';"%(filterStr)
#         # cursor.execute(sql)
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
#         current_app.logger.exception(e)
#         conn.rollback()

# xijiawei
# 模糊查询物料信息
def select_materialInfoByFilter(filterStr):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select materialCode,materialCode from materialInfo where materialCode like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            lock.release()
            return result
        cursor.execute("select materialCode,materialName from materialInfo where materialName like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            lock.release()
            return result
        cursor.execute("select materialCode,materialType from materialInfo where materialType like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            lock.release()
            return result
        lock.release()
        return None
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 添加或更新物料
def insertOrUpdate_materialInfo(materialCode, materialType, materialName, remark):
    conn = dbpool.connect()
    cursor = conn.cursor()
    # sql = "replace into materialInfo(materialCode, materialType, materialName, remark) value('%s','%s','%s','%s');" \
    #       % (materialCode, materialType, materialName, remark)
    try:
        lock.acquire()
        cursor.execute("select materialCode from materialInfo where materialCode='%s';"%materialCode)
        result = cursor.fetchall()
        if not result:
            cursor.execute("insert into materialInfo(materialCode, materialName, materialType, remark) value('%s','%s','%s','%s');" % (materialCode, materialName, materialType, remark))
        else:
            cursor.execute("update materialInfo set materialName='%s', materialType='%s', remark='%s' where materialCode='%s';" % (materialName, materialType, remark,materialCode))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 更新物料库存数量
def update_materialInfo(materialCode, materialName, materialType, operateNum, price,unit,supplierCode):
    conn = dbpool.connect()
    cursor = conn.cursor()
    sql = "update materialInfo set materialName='%s',materialType='%s',inventoryNum=inventoryNum+'%d',unit='%s',price='%f',inventoryMoney=inventoryMoney+'%d'*'%f',supplierCode='%s' where materialCode='%s';" \
          % (materialName, materialType, operateNum, unit, price, operateNum, price,supplierCode, materialCode)
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute(sql)
        # 更新余库存金额
        cursor.execute("update materialInfo set inventoryMoney=price*inventoryNum where materialCode='%s';" % (materialCode))
        # 更新成品费用
        cursor.execute("update materialsOfProduct mOP,materialInfo m set materialPrice=m.price,materialCost=m.price*materialNum where mOP.materialCode='%s' and mOP.materialCode=m.materialCode;" % materialCode)

        # 2020.11.19修改，库存物料价格修改，成品售价不变，利润变化
        # cursor.execute("update productInfo p, (select productCode,sum(materialCost+patchCost) sum from materialsOfProduct where productCode in (select distinct productCode from materialsOfProduct where materialCode='%s') group by productCode) mOP set price=(mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost+p.profit)*p.taxRate,totalCost=mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost,materialCost=mOP.sum where p.productCode=mOP.productCode;" % materialCode)
        cursor.execute("update productInfo p, (select productCode,sum(materialCost+patchCost) sum from materialsOfProduct where productCode in (select distinct productCode from materialsOfProduct where materialCode='%s') group by productCode) mOP set profit=(p.price/p.taxRate-mOP.sum-p.adminstrationCost-p.processCost-p.supplementaryCost-p.operatingCost),totalCost=mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost,materialCost=mOP.sum where p.productCode=mOP.productCode;" % materialCode)
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    except:
        conn.rollback()

# xijiawei
# 删除物料
def delete_materialByCode(materialCode):
    conn = dbpool.connect()
    cursor = conn.cursor()
    sql = "delete from materialInfo where materialCode='%s';" % (materialCode)
    try:
        lock.acquire()
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    except:
        conn.rollback()

# xijiawei
# 查询每个物料的最近3条出入库记录
def select_all_materialInOut():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select m.materialCode,materialInfo.materialName,materialInfo.materialType,m.isInOrOut,m.beforeinventoryNum,m.operateNum,m.unit,m.price,round(m.operateNum*m.price,2),m.supplierCode,m.documentNumber,date_format(m.documentTime,'%Y-%m-%d'),date_format(m.operateTime,'%Y-%m-%d %H:%i:%s.%f'),m.operatorName from (select a.* from materialInOut a where 3>(select count(*) from materialInOut b where b.materialCode=a.materialCode and b.operateTime>a.operateTime)) m left join materialInfo on m.materialCode=materialInfo.materialCode order by m.materialCode,m.operateTime desc;")
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询每个物料的最近3条出入库记录
def select_sum_materialInOut():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select isInOrOut,sum(operateNum),round(sum(operateNum*price),2) from materialInOut group by isInOrOut;")
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据时间段查询物料出入库记录
def select_all_materialInOutFilterByDate(startDate,endDate):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select materialInOut.materialCode,materialInfo.materialName,materialInfo.materialType,materialInOut.isInOrOut,materialInOut.beforeinventoryNum,materialInOut.operateNum,materialInOut.unit,materialInOut.price,round(materialInOut.operateNum*materialInOut.price,2),materialInOut.supplierCode,materialInOut.documentNumber,date_format(materialInOut.documentTime,'%%Y-%%m-%%d'),date_format(materialInOut.operateTime,'%%Y-%%m-%%d %%H:%%i:%%S.%%f'),materialInOut.operatorName from materialInOut, materialInfo where materialInOut.materialCode=materialInfo.materialCode and materialInOut.documentTime>='%s' and materialInOut.documentTime<='%s' order by materialInOut.materialCode,materialInOut.operateTime desc;" % (startDate, endDate))
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询每个物料的最近3条出入库记录
def select_sum_materialInOutFilterByDate(startDate, endDate):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select isInOrOut,sum(operateNum),round(sum(operateNum*price),2) from materialInOut where materialInOut.documentTime>='%s' and materialInOut.documentTime<='%s' group by isInOrOut;" % (startDate, endDate))
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据物料编码查询物料出入库记录
def select_materialInOutByCode(materialCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select * from materialInOut where materialCode='%s';" % materialCode)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：", e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 插入物料出入库记录
def insert_materialInOut(documentNumber,documentTime,materialCode,isInOrOut,operateNum,unit,price,supplierCode,operateTime,operatorName):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("select inventoryNum from materialInfo where materialCode='%s';"%(materialCode))
        result = cursor.fetchall()
        if result:
            beforeinventoryNum=result[0][0]
        else:
            beforeinventoryNum=0
        cursor.execute("insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplierCode,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" % (documentNumber, documentTime, materialCode, isInOrOut, beforeinventoryNum, operateNum, unit, price, supplierCode, operateTime, operatorName))

        # 更新供应商的应付款，只关心入库操作
        if isInOrOut==0:
            payable = price * operateNum
            # 更新供应商
            cursor.execute("select supplierCode from suppliers where supplierCode='%s';" % supplierCode)
            result = cursor.fetchall()
            if result:
                cursor.execute("update suppliers set payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s';" % (payable, operateTime, operatorName, supplierCode))
            else:
                cursor.execute("insert into suppliers (supplierCode, supplier, payable, payment, entryTime, entryClerk) values ('%s','%s','%f','%f','%s','%s')" % (supplierCode, supplierCode, payable, 0, operateTime, operatorName))

            # 更新应付款报表
            month = documentTime[0:7]
            cursor.execute("select supplierCode from payableReport where supplierCode='%s' and month='%s';" % (supplierCode, month))
            result = cursor.fetchall()
            if result:
                cursor.execute("update payableReport set addPayable=addPayable+'%f',payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month='%s';" % (payable, payable, operateTime, operatorName, supplierCode,month)) # 更新该月的addPayable
                cursor.execute("update payableReport set remainPayable=remainPayable+'%f',payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month>'%s';" % (payable, payable, operateTime, operatorName, supplierCode,month)) # 更新该月以后月份的remainPayable
            else:
                cursor.execute("select payable-payment from payableReport where supplierCode='%s' and month in (select max(month) from payableReport where supplierCode='%s' and month<'%s');" % (supplierCode, supplierCode, month))
                result = cursor.fetchall()
                if result:
                    remainPayable = result[0][0]
                else:
                    remainPayable = 0
                cursor.execute("insert into payableReport (supplierCode, month, remainPayable, addPayable, payable, payment, entryTime, entryClerk) value ('%s','%s','%f','%f','%f','%f','%s','%s');" % (supplierCode, month, remainPayable, payable, remainPayable + payable, 0, operateTime, operatorName))

            # 更新应付款明细报表
            cursor.execute("select supplierCode from payableReportGroupByMaterialCode where supplierCode='%s' and materialCode='%s' and month='%s';" % (supplierCode, materialCode, month))
            result = cursor.fetchall()
            if result:
                cursor.execute("update payableReportGroupByMaterialCode set materialNum=materialNum+'%d', addPayable=addPayable+'%f', payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and materialCode='%s' and month='%s';" % (operateNum, payable, payable, operateTime, operatorName, supplierCode, materialCode, month))
            else:
                cursor.execute("insert into payableReportGroupByMaterialCode (supplierCode, materialCode, month, materialNum, addPayable, payable, entryTime, entryClerk) value ('%s','%s','%s','%d','%f','%f','%s','%s');" % (supplierCode, materialCode, month, operateNum, payable, payable, operateTime, operatorName))

        # 执行SQL语句
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 更新物料出入库记录，更新相关物料出入库记录物料数量，并更新materialInfo表
def update_materialInOut(documentNumber, documentTime, isInOrOut, operateNum, unit, price, supplierCode, operateTime, operatorName, beforeInventoryNum):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        # cursor.execute("select materialCode,isInOrOut,operateNum,operateTime from materialInOut where documentNumber='%s';" % (documentNumber))
        # result = cursor.fetchall()
        # if result:
        #     materialCode=result[0][0]
        #     beforeIsInOrOut=result[0][1]
        #     beforeOperateNum=result[0][2]
        #     operateTime=result[0][3]
        #     if beforeIsInOrOut==0 and isInOrOut==0:
        #         cursor.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % ((operateNum-beforeOperateNum),materialCode,operateTime))
        #         # 更新materialInfo表
        #         cursor.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%d'*price where materialCode='%s';" % ((operateNum-beforeOperateNum), (operateNum-beforeOperateNum), materialCode))
        #     elif beforeIsInOrOut==1 and isInOrOut==0:
        #         cursor.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % ((operateNum+beforeOperateNum),materialCode,operateTime))
        #         # 更新materialInfo表
        #         cursor.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%d'*price where materialCode='%s';" % ((operateNum+beforeOperateNum), (operateNum+beforeOperateNum), materialCode))
        #     elif beforeIsInOrOut==0 and isInOrOut==1:
        #         cursor.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum-'%d' where materialCode='%s' and operateTime>'%s';" % ((operateNum+beforeOperateNum),materialCode,operateTime))
        #         # 更新materialInfo表
        #         cursor.execute("update materialInfo set inventoryNum=inventoryNum-'%d',inventoryMoney=inventoryMoney-'%d'*price where materialCode='%s';" % ((operateNum+beforeOperateNum), (operateNum+beforeOperateNum), materialCode))
        #     elif beforeIsInOrOut==1 and isInOrOut==1:
        #         cursor.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum-'%d' where materialCode='%s' and operateTime>'%s';" % ((operateNum-beforeOperateNum),materialCode,operateTime))
        #         # 更新materialInfo表
        #         cursor.execute("update materialInfo set inventoryNum=inventoryNum-'%d',inventoryMoney=inventoryMoney-'%d'*price where materialCode='%s';" % ((operateNum-beforeOperateNum), (operateNum-beforeOperateNum), materialCode))
        # sql = "update materialInOut set isInOrOut='%d',operateNum='%d',unit='%s',price='%f',supplierCode='%s' where documentNumber='%s';" \
        #           % (isInOrOut, operateNum, unit, price, supplierCode, documentNumber)
        # # 执行SQL语句
        # cursor.execute(sql)

        lock.acquire()
        cursor.execute("select materialCode,isInOrOut,price,operateNum,operateTime from materialInOut where documentNumber='%s';" % (documentNumber))
        result = cursor.fetchall()
        cursor.execute("delete from materialInOut where documentNumber='%s';" % (documentNumber))
        if result:
            materialCode=result[0][0]
            beforeIsInOrOut=result[0][1]
            beforePrice=result[0][2]
            beforeOperateNum=result[0][3]
            beforeOperateTime=result[0][4]
            if beforeIsInOrOut==0 and isInOrOut==0:
                # 更新materialInOut表（相当于撤销此条出入库记录，调整为最新）
                cursor.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % (-beforeOperateNum,materialCode,beforeOperateTime))
                # 更新materialInfo表
                cursor.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%f',unit='%s',price='%f',supplierCode='%s' where materialCode='%s';" % ((operateNum-beforeOperateNum), (operateNum*price-beforeOperateNum*beforePrice), unit, price, supplierCode, materialCode))
                # 插入materialInOut表
                cursor.execute("insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplierCode,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" % (documentNumber, documentTime, materialCode, isInOrOut, beforeInventoryNum-beforeOperateNum, operateNum, unit, price, supplierCode, operateTime, operatorName))
            elif beforeIsInOrOut==1 and isInOrOut==0:
                cursor.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % (beforeOperateNum,materialCode,beforeOperateTime))
                # 更新materialInfo表
                cursor.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%f',unit='%s',price='%f',supplierCode='%s' where materialCode='%s';" % ((operateNum+beforeOperateNum), (operateNum*price+beforeOperateNum*beforePrice), unit, price, supplierCode, materialCode))
                # 插入materialInOut表
                cursor.execute("insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplierCode,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" % (documentNumber, documentTime, materialCode, isInOrOut, beforeInventoryNum+beforeOperateNum, operateNum, unit, price, supplierCode, operateTime, operatorName))
            elif beforeIsInOrOut==0 and isInOrOut==1:
                cursor.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % (-beforeOperateNum,materialCode,beforeOperateTime))
                # 更新materialInfo表
                cursor.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%f',unit='%s',price='%f',supplierCode='%s' where materialCode='%s';" % ((-operateNum-beforeOperateNum), (-operateNum*price-beforeOperateNum*beforePrice), unit, price, supplierCode, materialCode))
                # 插入materialInOut表
                cursor.execute("insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplierCode,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" % (documentNumber, documentTime, materialCode, isInOrOut, beforeInventoryNum-beforeOperateNum, operateNum, unit, price, supplierCode, operateTime, operatorName))
            elif beforeIsInOrOut==1 and isInOrOut==1:
                cursor.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % (beforeOperateNum,materialCode,beforeOperateTime))
                # 更新materialInfo表
                cursor.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%f',unit='%s',price='%f',supplierCode='%s' where materialCode='%s';" % ((-operateNum+beforeOperateNum), (-operateNum*price+beforeOperateNum*beforePrice), unit, price, supplierCode, materialCode))
                # 插入materialInOut表
                cursor.execute("insert into materialInOut (documentNumber,documentTime,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplierCode,operateTime,operatorName)value('%s','%s','%s','%d','%d','%d','%s','%f','%s','%s','%s');" % (documentNumber, documentTime, materialCode, isInOrOut, beforeInventoryNum+beforeOperateNum, operateNum, unit, price, supplierCode, operateTime, operatorName))
            # 更新余库存金额
            cursor.execute("update materialInfo set inventoryMoney=price*inventoryNum where materialCode='%s';" % (materialCode))
            # 更新成品费用
            cursor.execute("update materialsOfProduct mOP,materialInfo m set materialPrice=m.price,materialCost=m.price*materialNum where mOP.materialCode='%s' and mOP.materialCode=m.materialCode;" % materialCode)
            cursor.execute("update productInfo p, (select productCode,sum(materialCost+patchCost) sum from materialsOfProduct where productCode in (select distinct productCode from materialsOfProduct where materialCode='%s') group by productCode) mOP set price=(mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost+p.profit)*p.taxRate,totalCost=mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost,materialCost=mOP.sum where p.productCode=mOP.productCode;" % materialCode)

            # 更新供应商的应付款，只关心入库操作
            if beforeIsInOrOut == 0 and isInOrOut == 0:
                payableDelta = operateNum*price-beforeOperateNum*beforePrice
            elif beforeIsInOrOut == 1 and isInOrOut == 0:
                payableDelta = operateNum*price
            elif beforeIsInOrOut == 0 and isInOrOut == 1:
                payableDelta = -beforeOperateNum*beforePrice
            month=documentTime[0:7]
            cursor.execute("update suppliers set payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s';" % (payableDelta, operateTime, operatorName, supplierCode))
            cursor.execute("update payableReport set addPayable=addPayable+'%f',payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month='%s';" % (payableDelta, payableDelta, operateTime, operatorName, supplierCode,month)) # 更新该月的addPayable
            cursor.execute("update payableReport set remainPayable=remainPayable+'%f',payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month>'%s';" % (payableDelta, payableDelta, operateTime, operatorName, supplierCode,month)) # 更新该月以后月份的remainPayable
            cursor.execute("update payableReportGroupByMaterialCode set payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and materialCode='%s' and month='%s';" % (payableDelta, operateTime, operatorName, supplierCode, materialCode, month))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 更新物料出入库记录，更新相关物料出入库记录物料数量，并更新materialInfo表
def update_materialInOutByCode(materialCode, differenceOperateNum, operateTime):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 更新materialInOut表
        cursor.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" %
                    (differenceOperateNum, materialCode, operateTime))
        # 更新materialInfo表
        cursor.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%d'*price where materialCode='%s';" %
                    (differenceOperateNum, differenceOperateNum, materialCode))
        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据单据号删除物料出入库记录，更新相关物料出入库记录物料数量，并更新materialInfo表
def delete_materialInOutByDocNum(documentNumber):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("select materialCode,isInOrOut,operateNum,operateTime,documentTime,supplierCode from materialInOut where documentNumber='%s';" % (documentNumber))
        materialInOutInfo = cursor.fetchall()
        if materialInOutInfo:
            materialCode = materialInOutInfo[0][0]
            isInOrOut = materialInOutInfo[0][1]
            operateNum = materialInOutInfo[0][2]
            operateTime = materialInOutInfo[0][3]
            documentTime = materialInOutInfo[0][4]
            supplierCode = materialInOutInfo[0][5]
            if isInOrOut == 0:
                cursor.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum-'%d' where materialCode='%s' and operateTime>'%s';" % (operateNum, materialCode, operateTime))
                # 更新materialInfo表
                cursor.execute("update materialInfo set inventoryNum=inventoryNum-'%d',inventoryMoney=inventoryMoney-'%d'*price where materialCode='%s';" % (operateNum, operateNum, materialCode))
            if isInOrOut == 1:
                cursor.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % (operateNum, materialCode, operateTime))
                # 更新materialInfo表
                cursor.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%d'*price where materialCode='%s';" % (operateNum, operateNum, materialCode))

            # 更新materialInfo表price
            cursor.execute(("select * from materialInOut a,(select materialCode,operateTime from materialInOut where documentNumber='%s') b where a.operateTime>b.operateTime and a.materialCode=b.materialCode;") % documentNumber)
            result = cursor.fetchall()  # 如果记录为此物料最新记录，则查询结果为空
            if not result:
                cursor.execute("delete from materialInOut where documentNumber='%s';" % (documentNumber))
                # cursor.execute(("select materialCode,price from materialInOut,(select a.materialCode as mCode,max(a.operateTime) as latest from materialInOut a,(select materialCode from materialInOut where documentNumber='%s') b where a.materialCode=b.materialCode) m where materialCode=m.mCode and operateTime=m.latest;") % documentNumber)
                cursor.execute(("select materialInOut.price from materialInOut,(select materialCode,max(operateTime) as latest from materialInOut where materialCode='%s') m where materialInOut.materialCode=m.materialCode and operateTime=m.latest;") % materialCode)
                price = cursor.fetchall()
                if price:
                    cursor.execute("update materialInfo set price='%f' where materialCode='%s';" % (price[0][0], materialCode))
            else:
                cursor.execute("delete from materialInOut where documentNumber='%s';" % (documentNumber))
            # 更新余库存金额
            cursor.execute("update materialInfo set inventoryMoney=price*inventoryNum where materialCode='%s';" % (materialCode))
            # 更新成品费用
            cursor.execute("update materialsOfProduct mOP,materialInfo m set materialPrice=m.price,materialCost=m.price*materialNum where mOP.materialCode='%s' and mOP.materialCode=m.materialCode;" % materialCode)
            cursor.execute("update productInfo p, (select productCode,sum(materialCost+patchCost) sum from materialsOfProduct where productCode in (select distinct productCode from materialsOfProduct where materialCode='%s') group by productCode) mOP set price=(mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost+p.profit)*p.taxRate,totalCost=mOP.sum+p.adminstrationCost+p.processCost+p.supplementaryCost+p.operatingCost,materialCost=mOP.sum where p.productCode=mOP.productCode;" % materialCode)

            # 更新供应商的应付款
            if isInOrOut == 0:
                cursor.execute(("select price from materialInfo where materialCode='%s';") % materialCode)
                price = cursor.fetchall()[0][0]
                payableDelta = -operateNum * price
                month = documentTime.strftime('%Y-%m')
                cursor.execute("update suppliers set payable=payable+'%f' where supplierCode='%s';" % (payableDelta, supplierCode))
                cursor.execute("update payableReport set addPayable=addPayable+'%f',payable=payable+'%f' where supplierCode='%s' and month='%s';" % (payableDelta, payableDelta, supplierCode, month)) # 更新该月的addPayable
                cursor.execute("update payableReport set remainPayable=remainPayable+'%f',payable=payable+'%f' where supplierCode='%s' and month>'%s';" % (payableDelta, payableDelta, supplierCode,month)) # 更新该月以后月份的remainPayable
                cursor.execute("update payableReportGroupByMaterialCode set materialNum=materialNum-'%d', payable=payable+'%f' where supplierCode='%s' and materialCode='%s' and month='%s';" % (operateNum, payableDelta, supplierCode, materialCode, month))

        # 提交到数据库执行
        conn.commit()
        lock.release()
        print("语句已经提交")
        return True
    # except:
    #     conn.rollback()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

##### 订单 #####

# xijiawei
# 查询所有订单
def select_concated_orders():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select orderCode, group_concat(distinct clientCode), group_concat(distinct orderDate), group_concat(productType), max(deliveryDate), (sum(deliveryNum)<=sum(deliveredNum)), group_concat(remark) from orders group by orderCode;")
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_concated_ordersByMonth(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select orderCode, group_concat(distinct clientCode), group_concat(distinct orderDate), group_concat(productType), date_format(max(deliveryDate),'%%Y-%%m-%%d'), (sum(deliveryNum)<=sum(deliveredNum)), group_concat(remark) from orders where date_format(orderDate,'%%Y-%%m')='%s' group by orderCode;" % month)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_orderByCode(orderCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select client, address, contact, telephone, date_format(orderDate,'%%Y-%%m-%%d'), productType, deliveryNum, date_format(deliveryDate,'%%Y-%%m-%%d'), deliveredNum, unit, price, orders.receivable, orders.remark from orders,clients where orderCode='%s' and orders.clientCode=clients.clientCode;" % orderCode)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_orderByCodeAndType(orderCode,productType):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select deliveryNum-deliveredNum,inventoryNum from orders,productInfo where orderCode='%s' and orders.productType='%s' and orders.productType=productInfo.productType;" % (orderCode, productType))
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_all_orderGroupByProductType():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select clientCode, group_concat(productType), group_concat(deliveryNum), group_concat(deliveredNum) from orderGroupByProductType group by clientCode;")
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_orderGroupByProductTypeByCode(clientCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select orderGroupByProductType.productType,orderGroupByProductType.unit,orderGroupByProductType.price,inventoryNum from orderGroupByProductType,productInfo where clientCode='%s' and orderGroupByProductType.productType=productInfo.productType;"%clientCode)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_receivableReportGroupByProductTypeByClientCodeAndProductType(clientCode, productType, month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select remainDeliveryNum,addDeliveryNum,deliveryNum,deliveredNum from receivableReportGroupByProductType where clientCode='%s' and productType='%s' and month='%s';"%(clientCode, productType, month))
        result = cursor.fetchall()
        lock.release()
        if not result:
            cursor.execute("select deliveryNum-deliveredNum from receivableReportGroupByProductType where clientCode='%s' and productType='%s' and month in (select max(month) from receivableReportGroupByProductType where clientCode='%s' and productType='%s' and month<'%s');"%(clientCode, productType, clientCode, productType, month))
            result = cursor.fetchall()
            if not result:
                remainDeliveryNum=0
            else:
                remainDeliveryNum=result[0][0]
            return [[remainDeliveryNum,0,remainDeliveryNum,0]]
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_orderGroupByProductTypeByClientCodeAndProductType(clientCode, productType):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select deliveryNum-deliveredNum,deliveredNum,p.inventoryNum from orderGroupByProductType orders, productInfo p where orders.clientCode='%s' and orders.productType='%s' and orders.productType=p.productType;" % (clientCode, productType))
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_deliveryGroupByProductTypeByClientCode(clientCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select deliveryCode, date_format(sendDate,'%%Y-%%m-%%d'), d.productType, unit, sendNum, d.price, sendNum*d.price, d.beforeDeliveryNum, d.beforeDeliveryNum-sendNum, d.remark from deliveryGroupByProductType d, productInfo p where d.clientCode='%s' and d.productType=p.productType order by deliveryCode;" % clientCode)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_deliveryGroupByProductTypeSumByClientCode(clientCode, productType, month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select date_format(sendDate,'%%Y-%%m') as month, sum(sendNum) from deliveryGroupByProductType where clientCode='%s' and productType='%s' and date_format(sendDate,'%%Y-%%m')='%s' group by month;" % (clientCode, productType, month))
        result = cursor.fetchall()
        lock.release()
        if result:
            return result[0][1]
        else:
            return 0
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def insert_order(orderCode, orderDate, clientCode, productType, deliveryNum, deliveryDate, unit, price, receivable, remark, entryTime, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()

        # （旧）
        # cursor.execute("insert into orders (orderCode, orderDate, clientCode, productType, deliveryNum, deliveryDate, deliveredNum, unit, price, receivable, remark, entryTime, entryClerk) values('%s','%s','%s','%s','%d','%s','%d','%s','%f','%f','%s','%s','%s');"%(orderCode, orderDate, clientCode, productType, deliveryNum, deliveryDate, 0, unit, price, receivable, remark, entryTime, entryClerk))
        # # 更新交易客户的应收款
        # cursor.execute("select clientCode from clients where clientCode='%s';"%clientCode)
        # result = cursor.fetchall()
        # if result:
        #     cursor.execute("update clients set receivable=receivable+'%f', entryTime='%s', entryClerk='%s' where clientCode='%s';" % (receivable, entryTime, entryClerk, clientCode))
        # else:
        #     cursor.execute("insert into clients (clientCode, client, receivable, receipt, entryTime, entryClerk) values ('%s','%s','%f','%f','%s','%s')" % (clientCode, clientCode, receivable, 0, entryTime, entryClerk))
        #
        # # 更新订单报表
        # month=orderDate[0:7]
        # cursor.execute("select clientCode from receivableReport where clientCode='%s' and month='%s';"%(clientCode,month))
        # result = cursor.fetchall()
        # if result:
        #     cursor.execute("update receivableReport set addReceivable=addReceivable+'%f',receivable=receivable+'%f', entryTime='%s', entryClerk='%s' where clientCode='%s' and month='%s';" % (receivable, receivable, entryTime, entryClerk, clientCode, month)) # 更新该月的addReceivable
        #     cursor.execute("update receivableReport set remainReceivable=remainReceivable+'%f',receivable=receivable+'%f', entryTime='%s', entryClerk='%s' where clientCode='%s' and month>'%s';" % (receivable, receivable, entryTime, entryClerk, clientCode, month)) # 更新该月以后月份的remainReceivable
        # else:
        #     # 方式一（可用不用）：要求每月都有报表数据
        #     # year_int = int(orderDate[0:4])
        #     # month_int = int(orderDate[5:7])
        #     # if month_int == 1:
        #     #     lastmonth = str(year_int - 1) + '-12'
        #     # else:
        #     #     lastmonth = orderDate[0:5] + str(month_int - 1)
        #     # cursor.execute("select receivable-receipt from receivableReport where clientCode='%s' and month='%s';" % (clientCode, lastmonth))
        #     # result = cursor.fetchall()
        #     # if result:
        #     #     remainReceivable=result[0][0]
        #     # else:
        #     #     remainReceivable=0
        #     # cursor.execute("insert into receivableReport (clientCode, month, remainReceivable, addReceivable, receivable, receipt, remark, entryTime, entryClerk) value ('%s','%s','%f','%f','%f','%f','%s','%s','%s');" % (clientCode, month, remainReceivable+receivable, receivable, remainReceivable+receivable, 0, remark, entryTime, entryClerk))
        #     # 方式二：允许一些月份空数据
        #     cursor.execute("select receivable-receipt from receivableReport where clientCode='%s' and month in (select max(month) from receivableReport where clientCode='%s' and month<'%s');" % (clientCode, clientCode, month))
        #     result = cursor.fetchall()
        #     if result:
        #         remainReceivable = result[0][0]
        #     else:
        #         remainReceivable = 0
        #     cursor.execute("insert into receivableReport (clientCode, month, remainReceivable, addReceivable, receivable, receipt, remark, entryTime, entryClerk) value ('%s','%s','%f','%f','%f','%f','%s','%s','%s');" % (clientCode, month, remainReceivable, receivable, remainReceivable + receivable, 0, remark, entryTime, entryClerk))
        #
        # # 更新orderGroupByProductType
        # cursor.execute("select clientCode from orderGroupByProductType where clientCode='%s' and productType='%s';"%(clientCode,productType))
        # result = cursor.fetchall()
        # if result:
        #     cursor.execute("update orderGroupByProductType set price='%f', deliveryNum=deliveryNum+'%f', receivable=receivable+'%f', remark=concat(remark,'%s'), entryTime='%s', entryClerk='%s' where clientCode='%s' and productType='%s';" % (price, deliveryNum, receivable, remark, entryTime, entryClerk, clientCode, productType))
        # else:
        #     cursor.execute("insert into orderGroupByProductType (clientCode, productType, unit, price, deliveryNum, deliveredNum, receivable, receipt, remark, entryTime, entryClerk) values ('%s','%s','%s','%f','%d','%d','%f','%f','%s','%s','%s');" % (clientCode, productType, unit, price, deliveryNum, 0, receivable, 0, remark, entryTime, entryClerk))
        #
        # # 更新receivableReportGroupByProductType
        # cursor.execute("select clientCode from receivableReportGroupByProductType where clientCode='%s' and productType='%s' and month='%s';"%(clientCode,productType,month))
        # result = cursor.fetchall()
        # if result:
        #     cursor.execute("update receivableReportGroupByProductType set addDeliveryNum=addDeliveryNum+'%d', deliveryNum=deliveryNum+'%d', addReceivable=addReceivable+'%f', receivable=receivable+'%f', remark=concat(remark,'%s'), entryTime='%s', entryClerk='%s' where clientCode='%s' and productType='%s' and month='%s';" % (deliveryNum, deliveryNum, receivable, receivable, remark, entryTime, entryClerk, clientCode, productType, month)) # 更新该月的addDeliveryNum和addReceivable
        #     cursor.execute("update receivableReportGroupByProductType set remainDeliveryNum=remainDeliveryNum+'%d', deliveryNum=deliveryNum+'%d', remainReceivable=remainReceivable+'%f', receivable=receivable+'%f', remark=concat(remark,'%s'), entryTime='%s', entryClerk='%s' where clientCode='%s' and productType='%s' and month>'%s';" % (deliveryNum, deliveryNum, receivable, receivable, remark, entryTime, entryClerk, clientCode, productType, month)) # 更新该月以后月份的remainDeliveryNum和remainReceivable
        # else:
        #     cursor.execute("select deliveryNum-deliveredNum,receivable-receipt from receivableReportGroupByProductType where clientCode='%s' and productType='%s' and month in (select max(month) from receivableReportGroupByProductType where clientCode='%s' and productType='%s' and month<'%s');" % (clientCode, productType, clientCode, productType, month))
        #     result = cursor.fetchall()
        #     if result:
        #         remainDeliveryNum = result[0][0]
        #         remainReceivable = result[0][1]
        #     else:
        #         remainDeliveryNum = 0
        #         remainReceivable = 0
        #     cursor.execute("insert into receivableReportGroupByProductType (clientCode, productType, month, remainDeliveryNum, addDeliveryNum, deliveryNum, deliveredNum, remainReceivable, addReceivable, receivable, receipt, remark, entryTime, entryClerk) value ('%s','%s','%s','%d','%d','%d','%d','%f','%f','%f','%f','%s','%s','%s');" % (clientCode, productType, month, remainDeliveryNum, deliveryNum, deliveryNum, 0, remainReceivable, receivable, remainReceivable + receivable, 0, remark, entryTime, entryClerk))

        # （新）
        cursor.execute("insert into orders (orderCode, orderDate, clientCode, productType, deliveryNum, deliveryDate, deliveredNum, unit, price, receivable, remark, entryTime, entryClerk) values('%s','%s','%s','%s','%d','%s','%d','%s','%f','%f','%s','%s','%s');"%(orderCode, orderDate, clientCode, productType, deliveryNum, deliveryDate, 0, unit, price, 0, remark, entryTime, entryClerk))
        # 更新交易客户信息
        month = orderDate[0:7]
        cursor.execute("select clientCode from clients where clientCode='%s';"%clientCode)
        result = cursor.fetchall()
        if not result:
            cursor.execute("insert into clients (clientCode, client, entryTime, entryClerk) values ('%s','%s','%s','%s');" % (clientCode, clientCode, entryTime, entryClerk))
        # 更新orderGroupByProductType
        cursor.execute("select clientCode from orderGroupByProductType where clientCode='%s' and productType='%s';"%(clientCode,productType))
        result = cursor.fetchall()
        if result:
            cursor.execute("update orderGroupByProductType set price='%f', deliveryNum=deliveryNum+'%f', remark=concat(remark,'%s'), entryTime='%s', entryClerk='%s' where clientCode='%s' and productType='%s';" % (price, deliveryNum, remark, entryTime, entryClerk, clientCode, productType))
        else:
            cursor.execute("insert into orderGroupByProductType (clientCode, productType, unit, price, deliveryNum, deliveredNum, remark, entryTime, entryClerk) values ('%s','%s','%s','%f','%d','%d','%s','%s','%s');" % (clientCode, productType, unit, price, deliveryNum, 0, remark, entryTime, entryClerk))
        # 更新receivableReportGroupByProductType
        cursor.execute("select clientCode from receivableReportGroupByProductType where clientCode='%s' and productType='%s' and month='%s';"%(clientCode,productType,month))
        result = cursor.fetchall()
        if result:
            cursor.execute("update receivableReportGroupByProductType set addDeliveryNum=addDeliveryNum+'%d', deliveryNum=deliveryNum+'%d', price='%f', remark=concat(remark,'%s'), entryTime='%s', entryClerk='%s' where clientCode='%s' and productType='%s' and month='%s';" % (deliveryNum, deliveryNum, price, remark, entryTime, entryClerk, clientCode, productType, month)) # 更新该月的addDeliveryNum和addReceivable
            cursor.execute("update receivableReportGroupByProductType set remainDeliveryNum=remainDeliveryNum+'%d', deliveryNum=deliveryNum+'%d', remark=concat(remark,'%s'), entryTime='%s', entryClerk='%s' where clientCode='%s' and productType='%s' and month>'%s';" % (deliveryNum, deliveryNum, remark, entryTime, entryClerk, clientCode, productType, month)) # 更新该月以后月份的remainDeliveryNum和remainReceivable
        else:
            cursor.execute("select deliveryNum-deliveredNum,receivable-receipt from receivableReportGroupByProductType where clientCode='%s' and productType='%s' and month in (select max(month) from receivableReportGroupByProductType where clientCode='%s' and productType='%s' and month<'%s');" % (clientCode, productType, clientCode, productType, month))
            result = cursor.fetchall()
            if result:
                remainDeliveryNum = result[0][0]
                remainReceivable = result[0][1]
            else:
                remainDeliveryNum = 0
                remainReceivable = 0
            cursor.execute("insert into receivableReportGroupByProductType (clientCode, productType, month, remainDeliveryNum, addDeliveryNum, deliveryNum, deliveredNum, price, remainReceivable, addReceivable, receivable, receipt, remark, entryTime, entryClerk) value ('%s','%s','%s','%d','%d','%d','%d','%f','%f','%f','%f','%f','%s','%s','%s');" % (clientCode, productType, month, remainDeliveryNum, deliveryNum, remainDeliveryNum + deliveryNum, 0, price, remainReceivable, 0, remainReceivable, 0, remark, entryTime, entryClerk))
        # 更新deliveryGroupByProductType
        cursor.execute("update deliveryGroupByProductType set beforeDeliveryNum=beforeDeliveryNum+'%d' where clientCode='%s' and productType='%s' and date_format(entryTime,'%%Y-%%m')>='%s';"%(deliveryNum, clientCode, productType, orderDate[0:7]))

        conn.commit()
        lock.release()
        return
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 删除订单
def delete_order(orderCode):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # （旧）
        # cursor.execute("update clients,(select group_concat(distinct clientCode) as cliCode,sum(receivable) as sumReceivable from orders where orderCode='%s' group by orderCode) as t set receivable=receivable-t.sumReceivable where clients.clientCode=t.cliCode;" % (orderCode))
        # cursor.execute("update receivableReport,(select group_concat(distinct clientCode) as cliCode, date_format(group_concat(distinct orderDate),'%%Y-%%m') as cliDate, sum(receivable) as sumReceivable from orders where orderCode='%s' group by orderCode) as t set addReceivable=addReceivable-t.sumReceivable,receivable=receivable-t.sumReceivable where receivableReport.clientCode=t.cliCode and receivableReport.month=t.cliDate;" % (orderCode)) # 更新该月的addReceivable
        # cursor.execute("update receivableReport,(select group_concat(distinct clientCode) as cliCode, date_format(group_concat(distinct orderDate),'%%Y-%%m') as cliDate, sum(receivable) as sumReceivable from orders where orderCode='%s' group by orderCode) as t set remainReceivable=remainReceivable-t.sumReceivable,receivable=receivable-t.sumReceivable where receivableReport.clientCode=t.cliCode and receivableReport.month>t.cliDate;" % (orderCode)) # 更新该月以后月份的remainReceivable
        # cursor.execute("update orderGroupByProductType a,orders b set a.deliveryNum=a.deliveryNum-b.deliveryNum,a.receivable=a.receivable-b.receivable where b.orderCode='%s' and a.clientCode=b.clientCode and a.productType=b.productType;" % (orderCode))
        # cursor.execute("update receivableReportGroupByProductType a,orders b set a.addDeliveryNum=a.addDeliveryNum-b.deliveryNum,a.deliveryNum=a.deliveryNum-b.deliveryNum,a.addReceivable=a.addReceivable-b.receivable,a.receivable=a.receivable-b.receivable where b.orderCode='%s' and a.clientCode=b.clientCode and a.productType=b.productType and a.month=date_format(b.orderDate,'%%Y-%%m');" % (orderCode)) # 更新该月的addDeliveryNum和addReceivable
        # cursor.execute("update receivableReportGroupByProductType a,orders b set a.remainDeliveryNum=a.remainDeliveryNum-b.deliveryNum,a.deliveryNum=a.deliveryNum-b.deliveryNum,a.remainReceivable=a.remainReceivable-b.receivable,a.receivable=a.receivable-b.receivable where b.orderCode='%s' and a.clientCode=b.clientCode and a.productType=b.productType and a.month>date_format(b.orderDate,'%%Y-%%m');" % (orderCode)) # 更新该月以后月份的remainDeliveryNum和remainReceivable

        # （新）
        # cursor.execute("update orderGroupByProductType a,orders b set a.deliveryNum=a.deliveryNum-b.deliveryNum where b.orderCode='%s' and a.clientCode=b.clientCode and a.productType=b.productType;" % (orderCode))
        # cursor.execute("update deliveryGroupByProductType a,orders b set a.beforeDeliveryNum=a.beforeDeliveryNum-b.deliveryNum where b.orderCode='%s' and a.clientCode=b.clientCode and a.productType=b.productType and date_format(a.entryTime,'%%Y-%%m')>=date_format(b.orderDate,'%%Y-%%m');" % (orderCode)) # 更新此订单日期当月出货记录的beforeDeliveryNum
        # cursor.execute("update receivableReportGroupByProductType a,orders b set a.addDeliveryNum=a.addDeliveryNum-b.deliveryNum,a.deliveryNum=a.deliveryNum-b.deliveryNum where b.orderCode='%s' and a.clientCode=b.clientCode and a.productType=b.productType and a.month=date_format(b.orderDate,'%%Y-%%m');" % (orderCode)) # 更新该月的addDeliveryNum和addReceivable
        # cursor.execute("update receivableReportGroupByProductType a,orders b set a.remainDeliveryNum=a.remainDeliveryNum-b.deliveryNum,a.deliveryNum=a.deliveryNum-b.deliveryNum where b.orderCode='%s' and a.clientCode=b.clientCode and a.productType=b.productType and a.month>date_format(b.orderDate,'%%Y-%%m');" % (orderCode)) # 更新该月以后月份的remainDeliveryNum和remainReceivable

        cursor.execute("select distinct clientCode cliCode from orders where orderCode='%s';"%orderCode)
        result=cursor.fetchall()
        cursor.execute("select count(distinct orderCode) from orders where clientCode='%s';" % result[0][0])
        if cursor.fetchall()[0][0]==1:
            cursor.execute("delete from orderGroupByProductType where clientCode='%s';" % result[0][0])
            cursor.execute("delete from deliveryGroupByProductType where clientCode='%s';" % result[0][0]) # 更新此订单日期当月出货记录的beforeDeliveryNum
            cursor.execute("delete from receivableReportGroupByProductType where clientCode='%s';" % result[0][0]) # 更新该月的addDeliveryNum和addReceivable
        else:
            cursor.execute("update orderGroupByProductType a,orders b set a.deliveryNum=a.deliveryNum-b.deliveryNum where b.orderCode='%s' and a.clientCode=b.clientCode and a.productType=b.productType;" % (orderCode))
            cursor.execute("update deliveryGroupByProductType a,orders b set a.beforeDeliveryNum=a.beforeDeliveryNum-b.deliveryNum where b.orderCode='%s' and a.clientCode=b.clientCode and a.productType=b.productType and date_format(a.entryTime,'%%Y-%%m')>=date_format(b.orderDate,'%%Y-%%m');" % (orderCode)) # 更新此订单日期当月出货记录的beforeDeliveryNum
            cursor.execute("update receivableReportGroupByProductType a,orders b set a.addDeliveryNum=a.addDeliveryNum-b.deliveryNum,a.deliveryNum=a.deliveryNum-b.deliveryNum where b.orderCode='%s' and a.clientCode=b.clientCode and a.productType=b.productType and a.month=date_format(b.orderDate,'%%Y-%%m');" % (orderCode)) # 更新该月的addDeliveryNum和addReceivable
            cursor.execute("update receivableReportGroupByProductType a,orders b set a.remainDeliveryNum=a.remainDeliveryNum-b.deliveryNum,a.deliveryNum=a.deliveryNum-b.deliveryNum where b.orderCode='%s' and a.clientCode=b.clientCode and a.productType=b.productType and a.month>date_format(b.orderDate,'%%Y-%%m');" % (orderCode)) # 更新该月以后月份的remainDeliveryNum和remainReceivable

        cursor.execute("delete from orders where orderCode='%s';"%(orderCode))
        conn.commit()
        lock.release()
        return
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

##### 出货 #####

# xijiawei
# 查询所有订单
def select_deliveryByCode(deliveryCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select clients.client, clients.address, clients.contact, clients.telephone, orders.orderDate, orders.productType, deliveryNum, date_format(deliveryDate,'%%Y-%%m-%%d'), productInfo.unit, productInfo.price, date_format(sendDate,'%%Y-%%m-%%d'), sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, productInfo.inventoryNum, productInfo.inventoryNum-sendNum, delivery.remark, delivery.entryClerk from delivery,orders,clients,productInfo where deliveryCode='%s' and delivery.orderCode=orders.orderCode and delivery.productType=orders.productType and delivery.clientCode=clients.clientCode and delivery.productType=productInfo.productType;" % deliveryCode)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询某个订单的所有出货记录（弃用），因为此方式可能会查询出某些客户0条出货记录，这样查询结果里就没有该客户，但是实际要求是希望每个客户才能出现在查询结果里，即使该客户没有出货记录
def select_deliveryWithOrderByCode(orderCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select orders.productType, orders.deliveryNum, date_format(deliveryDate,'%%Y-%%m-%%d'), deliveryCode, sendDate, sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, productInfo.inventoryNum,productInfo.inventoryNum-sendNum,delivery.remark, orders.clientCode, date_format(orderDate,'%Y-%m-%d') from orders,delivery,productInfo where orders.orderCode='%s' and orders.orderCode=delivery.orderCode and orders.productType=productInfo.productType;" % orderCode)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_deliveryByOrderCodeAndProductType(orderCode, productType):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select deliveryCode, date_format(sendDate,'%%Y-%%m-%%d'), sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, productInfo.inventoryNum, productInfo.inventoryNum-sendNum, delivery.remark from delivery,productInfo where orderCode='%s' and delivery.productType='%s' and delivery.productType=productInfo.productType;" % (orderCode,productType))
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_deliveryGroupByProductTypeByCode(deliveryCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select clients.client, clients.address, clients.contact, clients.telephone, date_format(d.sendDate,'%%Y-%%m-%%d'), d.productType, og.unit, og.price, sendNum, d.remark, d.entryClerk from deliveryGroupByProductType d,orderGroupByProductType og,clients where deliveryCode='%s' and d.clientCode=og.clientCode and d.productType=og.productType and d.clientCode=clients.clientCode;" % deliveryCode)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_deliveryGroupByProductTypeByClientCodeAndProductType(clientCode, productType, month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select deliveryCode, date_format(sendDate,'%%Y-%%m-%%d'), sendNum, beforeDeliveryNum, beforeDeliveryNum-sendNum, remark from deliveryGroupByProductType where clientCode='%s' and productType='%s' and date_format(sendDate,'%%Y-%%m')='%s';" % (clientCode, productType, month))
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 插入订单出货
def insert_delivery(deliveryCode, orderCode, productType, beforeDeliveryNum, sendDate, sendNum, price, remark, clientCode, client, address, contact, telephone, entryTime, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("insert into delivery (deliveryCode, orderCode, productType, beforeDeliveryNum, sendDate, sendNum, remark, clientCode, entryTime, entryClerk) values('%s','%s','%s','%d','%s','%d','%s','%s','%s','%s');"%(deliveryCode, orderCode, productType, beforeDeliveryNum, sendDate, sendNum, remark, clientCode, entryTime, entryClerk))
        cursor.execute("insert into deliveryGroupByProductType (deliveryCode, clientCode, productType, beforeDeliveryNum, sendDate, sendNum, remark, entryTime, entryClerk) values('%s','%s','%s','%d','%s','%d','%s','%s','%s');"%(deliveryCode, clientCode, productType, beforeDeliveryNum, sendDate, sendNum, remark, entryTime, entryClerk))
        cursor.execute("update orders set deliveredNum=deliveredNum+'%d' where orderCode='%s' and productType='%s';"%(sendNum, orderCode, productType))
        cursor.execute("update orderGroupByProductType set deliveredNum=deliveredNum+'%d' where clientCode='%s' and productType='%s';"%(sendNum, clientCode, productType))

        # # 更新receivableReportGroupByProductType（旧）
        # cursor.execute("update receivableReportGroupByProductType set deliveredNum=deliveredNum+'%d' where clientCode='%s' and productType='%s' and month='%s';"%(sendNum, clientCode, productType, sendDate[0:7]))
        # cursor.execute("update receivableReportGroupByProductType set remainReceivable=remainReceivable-'%d',deliveredNum=deliveryNum-'%d' where clientCode='%s' and productType='%s' and month>'%s';"%(sendNum, sendNum, clientCode, productType, sendDate[0:7]))
        # cursor.execute("update clients set client='%s', contact='%s', address='%s', telephone='%s' where clientCode='%s';" % (client, contact, address, telephone, clientCode))

        # 更新receivableReport和receivableReportGroupByProductType（新）
        month=sendDate[0:7]
        receivable=sendNum*price
        cursor.execute("select clientCode from receivableReport where clientCode='%s' and month='%s';"%(clientCode,month))
        result = cursor.fetchall()
        if result:
            cursor.execute("update receivableReport set addReceivable=addReceivable+'%f',receivable=receivable+'%f', entryTime='%s', entryClerk='%s' where clientCode='%s' and month='%s';" % (receivable, receivable, entryTime, entryClerk, clientCode, month))
        else:
            cursor.execute("select receivable-receipt from receivableReport where clientCode='%s' and month in (select max(month) from receivableReport where clientCode='%s' and month<'%s');" % (clientCode, clientCode, month))
            result = cursor.fetchall()
            if result:
                remainReceivable = result[0][0]
            else:
                remainReceivable = 0
            cursor.execute("insert into receivableReport (clientCode, month, remainReceivable, addReceivable, receivable, receipt, remark, entryTime, entryClerk) value ('%s','%s','%f','%f','%f','%f','%s','%s','%s');" % (clientCode, month, remainReceivable, receivable, remainReceivable + receivable, 0, remark, entryTime, entryClerk))
        cursor.execute("update receivableReportGroupByProductType set addReceivable=addReceivable+'%f', receivable=receivable+'%f', remark=concat(remark,'%s'), entryTime='%s', entryClerk='%s' where clientCode='%s' and productType='%s' and month='%s';" % (receivable, receivable, remark, entryTime, entryClerk, clientCode, productType, month))
        cursor.execute("update clients set client='%s', contact='%s', address='%s', telephone='%s',receivable=receivable+'%f' where clientCode='%s';" % (client, contact, address, telephone, receivable, clientCode))

        conn.commit()
        lock.release()
        return
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 插入客户出货
def insert_deliveryGroupByProductType(deliveryCode, clientCode, productType, beforeDeliveryNum, sendDate, sendNum, price, remark, client, address, contact, telephone, entryTime, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("insert into deliveryGroupByProductType (deliveryCode, clientCode, productType, beforeDeliveryNum, sendDate, sendNum, price, remark, entryTime, entryClerk) values('%s','%s','%s','%d','%s','%d','%f','%s','%s','%s');"%(deliveryCode, clientCode, productType, beforeDeliveryNum, sendDate, sendNum, price, remark, entryTime, entryClerk))

        # # 更新receivableReportGroupByProductType（旧）
        # cursor.execute("update orderGroupByProductType set deliveredNum=deliveredNum+'%d' where clientCode='%s' and productType='%s';"%(sendNum,clientCode,productType))
        # cursor.execute("update receivableReportGroupByProductType set deliveredNum=deliveredNum+'%d' where clientCode='%s' and productType='%s' and month='%s';" % (sendNum, clientCode, productType,sendDate[0:7]))
        # cursor.execute("update receivableReportGroupByProductType set remainDeliveryNum=remainDeliveryNum-'%d',deliveredNum=deliveryNum-'%d' where clientCode='%s' and productType='%s' and month>'%s';" % (sendNum, sendNum, clientCode, productType,sendDate[0:7]))
        # cursor.execute("update clients set client='%s', contact='%s', address='%s', telephone='%s' where clientCode='%s';" % (client, contact, address, telephone, clientCode))

        # 更新orderGroupByProductType、receivableReport和receivableReportGroupByProductType（新）
        receivable=sendNum*price
        cursor.execute("update orderGroupByProductType set deliveredNum=deliveredNum+'%d',receivable=receivable+'%f' where clientCode='%s' and productType='%s';"%(sendNum, receivable, clientCode, productType))
        month=sendDate[0:7]
        cursor.execute("select clientCode from receivableReport where clientCode='%s' and month='%s';"%(clientCode,month))
        result = cursor.fetchall()
        if result:
            cursor.execute("update receivableReport set addReceivable=addReceivable+'%f',receivable=receivable+'%f', entryTime='%s', entryClerk='%s' where clientCode='%s' and month='%s';" % (receivable, receivable, entryTime, entryClerk, clientCode, month))
        else:
            cursor.execute("select receivable-receipt from receivableReport where clientCode='%s' and month in (select max(month) from receivableReport where clientCode='%s' and month<'%s');" % (clientCode, clientCode, month))
            result = cursor.fetchall()
            if result:
                remainReceivable = result[0][0]
            else:
                remainReceivable = 0
            cursor.execute("insert into receivableReport (clientCode, month, remainReceivable, addReceivable, receivable, receipt, remark, entryTime, entryClerk) value ('%s','%s','%f','%f','%f','%f','%s','%s','%s');" % (clientCode, month, remainReceivable, receivable, remainReceivable + receivable, 0, remark, entryTime, entryClerk))

        # cursor.execute("update receivableReportGroupByProductType set deliveredNum=deliveredNum+'%d', addReceivable=addReceivable+'%f', receivable=receivable+'%f', price='%f', remark=concat(remark,'%s'), entryTime='%s', entryClerk='%s' where clientCode='%s' and productType='%s' and month='%s';" % (sendNum, receivable, receivable, price, remark, entryTime, entryClerk, clientCode, productType, month))
        # 更新receivableReportGroupByProductType
        cursor.execute("select clientCode from receivableReportGroupByProductType where clientCode='%s' and productType='%s' and month='%s';"%(clientCode,productType,month))
        result = cursor.fetchall()
        if result:
            cursor.execute("update receivableReportGroupByProductType set deliveredNum=deliveredNum+'%d', addReceivable=addReceivable+'%f', receivable=receivable+'%f', price='%f', remark=concat(remark,'%s'), entryTime='%s', entryClerk='%s' where clientCode='%s' and productType='%s' and month='%s';" % (sendNum, receivable, receivable, price, remark, entryTime, entryClerk, clientCode, productType, month)) # 更新该月的addDeliveryNum和addReceivable
            cursor.execute("update receivableReportGroupByProductType set remainDeliveryNum=remainDeliveryNum-'%d', deliveryNum=deliveryNum-'%d', remainReceivable=remainReceivable+'%f', receivable=receivable+'%f', remark=concat(remark,'%s'), entryTime='%s', entryClerk='%s' where clientCode='%s' and productType='%s' and month>'%s';" % (sendNum, sendNum, receivable, receivable, remark, entryTime, entryClerk, clientCode, productType, month)) # 更新该月以后月份的remainDeliveryNum和remainReceivable
        else:
            cursor.execute("select deliveryNum-deliveredNum,receivable-receipt from receivableReportGroupByProductType where clientCode='%s' and productType='%s' and month in (select max(month) from receivableReportGroupByProductType where clientCode='%s' and productType='%s' and month<'%s');" % (clientCode, productType, clientCode, productType, month))
            result = cursor.fetchall()
            if result:
                remainDeliveryNum = result[0][0]
                remainReceivable = result[0][1]
            else:
                remainDeliveryNum = 0
                remainReceivable = 0
            cursor.execute("insert into receivableReportGroupByProductType (clientCode, productType, month, remainDeliveryNum, addDeliveryNum, deliveryNum, deliveredNum, price, remainReceivable, addReceivable, receivable, receipt, remark, entryTime, entryClerk) value ('%s','%s','%s','%d','%d','%d','%d','%f','%f','%f','%f','%f','%s','%s','%s');" % (clientCode, productType, month, remainDeliveryNum, 0, remainDeliveryNum, sendNum, price, remainReceivable, receivable, remainReceivable + receivable, 0, remark, entryTime, entryClerk))

        cursor.execute("update clients set client='%s', contact='%s', address='%s', telephone='%s',receivable=receivable+'%f' where clientCode='%s';" % (client, contact, address, telephone, receivable, clientCode))
        cursor.execute("update productInfo set inventoryNum=inventoryNum-'%d' where productType='%s';" % (sendNum, productType))

        conn.commit()
        lock.release()
        return
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 删除订单
def delete_deliveryGroupByProductType(deliveryCode):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("update clients,(select group_concat(distinct clientCode) as cliCode,sum(sendNum*price) as sumReceivable from deliveryGroupByProductType where deliveryCode='%s' group by deliveryCode) as t set receivable=receivable-t.sumReceivable where clients.clientCode=t.cliCode;" % (deliveryCode))
        cursor.execute("update receivableReport,(select group_concat(distinct clientCode) as cliCode, date_format(group_concat(distinct sendDate),'%%Y-%%m') as sndDate, sum(sendNum*price) as sumReceivable from deliveryGroupByProductType where deliveryCode='%s' group by deliveryCode) as t set addReceivable=addReceivable-t.sumReceivable,receivable=receivable-t.sumReceivable where receivableReport.clientCode=t.cliCode and receivableReport.month=t.sndDate;" % (deliveryCode)) # 更新该月的addReceivable
        cursor.execute("update receivableReport,(select group_concat(distinct clientCode) as cliCode, date_format(group_concat(distinct sendDate),'%%Y-%%m') as sndDate, sum(sendNum*price) as sumReceivable from deliveryGroupByProductType where deliveryCode='%s' group by deliveryCode) as t set remainReceivable=remainReceivable-t.sumReceivable,receivable=receivable-t.sumReceivable where receivableReport.clientCode=t.cliCode and receivableReport.month>t.sndDate;" % (deliveryCode)) # 更新该月以后月份的remainReceivable
        cursor.execute("update orderGroupByProductType a,deliveryGroupByProductType b set a.deliveredNum=a.deliveredNum-b.sendNum,a.receivable=a.receivable-b.sendNum*b.price where b.deliveryCode='%s' and a.clientCode=b.clientCode and a.productType=b.productType;" % (deliveryCode))
        cursor.execute("update receivableReportGroupByProductType a,deliveryGroupByProductType b set a.deliveredNum=a.deliveredNum-b.sendNum,a.addReceivable=a.addReceivable-b.sendNum*b.price,a.receivable=a.receivable-b.sendNum*b.price where b.deliveryCode='%s' and a.clientCode=b.clientCode and a.productType=b.productType and a.month=date_format(b.sendDate,'%%Y-%%m');" % (deliveryCode))
        cursor.execute("update productInfo a,deliveryGroupByProductType b set a.inventoryNum=a.inventoryNum+b.sendNum where b.deliveryCode='%s' and a.productType=b.productType;" % (deliveryCode))
        cursor.execute("update deliveryGroupByProductType a,(select productType as prdType,entryTime as enTime, sendNum as sndNum from deliveryGroupByProductType where deliveryCode='%s') b set a.beforeDeliveryNum=a.beforeDeliveryNum+b.sndNum where a.productType=b.prdType and a.entryTime>b.enTime;" % (deliveryCode)) # 更新此次出货日期之后出货记录的beforeDeliveryNum
        cursor.execute("delete from deliveryGroupByProductType where deliveryCode='%s';" % (deliveryCode))
        conn.commit()
        lock.release()
        return
    except Exception as e:
        print("数据库操作异常：", e)
        current_app.logger.exception(e)
        conn.rollback()


##### 收款 #####

# xijiawei
# 查询所有订单
def select_all_clients():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select clientCode, historyReceivable, receivable, receipt, receivable-receipt from clients;")
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 模糊查询物料信息
def select_clientInfoByFilter(filterStr):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select clientCode from clients where clientCode like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            lock.release()
            return result
        cursor.execute("select clientCode from clients where client like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            lock.release()
            return result
        lock.release()
        return None
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_clientByCode(clientCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select client, address, contact, telephone  from clients where clientCode='%s';" % clientCode)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_receiptsJournal(clientCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select receiptCode,date_format(receiptDate,'%%Y-%%m-%%d'),beforeReceivable,receipt,remark from receiptsJournal where clientCode='%s';" % clientCode)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_receiptsJournalSum(clientCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select round(sum(receipt),2) from receiptsJournal where clientCode='%s' group by clientCode;" % clientCode)
        result = cursor.fetchall()
        lock.release()
        if result:
            return result[0][0]
        else:
            return 0
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有客户应收款月度报表（暂不用）
def select_all_receivableReport(month):
    try:
        clients = select_all_clients()
        result = []
        for i in clients:
            receivable = select_receivableReportByCode(i[0], month)
            result.append(receivable[0])
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)

# xijiawei
# 查询所有订单
def select_receivableReportByCode(clientCode, month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select clientCode,round(remainReceivable,2),round(addReceivable,2),round(receivable,2),round(receipt,2),remark from receivableReport where clientCode='%s' and month='%s';" % (clientCode, month))
        result = cursor.fetchall()
        if not result:
            cursor.execute("select round(receivable-receipt,2) from receivableReport where clientCode='%s' and month in (select max(month) from receivableReport where clientCode='%s' and month<'%s');" % (clientCode, clientCode, month))
            remainReceivableResult = cursor.fetchall()
            if remainReceivableResult:
                remainReceivable = remainReceivableResult[0][0]
            else:
                cursor.execute("select historyReceivable from clients where clientCode='%s';" % (clientCode))
                remainReceivable = cursor.fetchall()[0][0]
            result=[[clientCode,remainReceivable,0,remainReceivable,0,'']]
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_receivableReportGroupByProductTypeByCode(clientCode, month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        # （旧）
        # cursor.execute("select r.productType, r.addDeliveryNum, p.price, r.addReceivable, r.remark from receivableReportGroupByProductType r,productInfo p where clientCode='%s' and month='%s' and r.productType=p.productType;" % (clientCode, month))
        # （新）
        cursor.execute("select clientCode, productType, deliveredNum, price, addReceivable, remark from receivableReportGroupByProductType where clientCode='%s' and month='%s';" % (clientCode, month))
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_all_receivableReportGroupByProductType(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select clientCode, productType, deliveredNum, price, addReceivable, remark from receivableReportGroupByProductType where month='%s';" % (month))
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def insert_receiptsJournal(clientCode,receiptDate,beforeReceivable,receipt,remark,entryTime,entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        receiptCode="R"+datetime.now().strftime('%Y%m%d%H%M%S%f')[0:16] # 使用时间戳生成唯一代号
        cursor.execute("insert into receiptsJournal (receiptCode,clientCode,receiptDate,beforeReceivable,receipt,remark,entryTime,entryClerk) values('%s','%s','%s','%f','%f','%s','%s','%s');"%(receiptCode,clientCode,receiptDate,beforeReceivable,receipt,remark,entryTime,entryClerk))
        cursor.execute("update clients set receipt=receipt+'%f', entryTime='%s', entryClerk='%s' where clientCode='%s';" % (receipt, entryTime, entryClerk, clientCode))

        # 更新订单报表
        # cursor.execute("update receivableReport set receipt=receipt+'%f', entryTime='%s', entryClerk='%s' where clientCode='%s' and month='%s';" % (receipt, entryTime, entryClerk, clientCode,receiptDate[0:7]))
        month=entryTime[0:7]
        cursor.execute("select receipt from receivableReport where clientCode='%s' and month='%s';" % (clientCode, month))
        result = cursor.fetchall()
        if result:
            cursor.execute("update receivableReport set receipt=receipt+'%f', entryTime='%s', entryClerk='%s' where clientCode='%s' and month='%s';" % (receipt, entryTime, entryClerk, clientCode, receiptDate[0:7]))
        else:
            cursor.execute("select receivable-receipt from receivableReport where clientCode='%s' and month in (select max(month) from receivableReport where clientCode='%s' and month<'%s');" % (clientCode, clientCode, month))
            result = cursor.fetchall()
            if result:
                remainReceivable = result[0][0]
            else:
                remainReceivable = 0
            cursor.execute("insert into receivableReport (clientCode, month, remainReceivable, addReceivable, receivable, receipt, remark, entryTime, entryClerk) value ('%s','%s','%f','%f','%f','%f','%s','%s','%s');" % (clientCode, month, remainReceivable, 0, remainReceivable, receipt, remark, entryTime, entryClerk))

        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def delete_receiptsJournal(receiptCode):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("update receivableReport,(select clientCode as cliCode, date_format(receiptDate,'%%Y-%%m') as month, receipt as rct from receiptsJournal where receiptCode='%s') rj set receipt=receipt-rj.rct where clientCode=rj.cliCode and receivableReport.month=rj.month;" % receiptCode)
        cursor.execute("update receivableReport,(select clientCode as cliCode, date_format(receiptDate,'%%Y-%%m') as month, receipt as rct from receiptsJournal where receiptCode='%s') rj set remainReceivable=remainReceivable+rj.rct, receivable=receivable+rj.rct where clientCode=rj.cliCode and receivableReport.month>rj.month;" % receiptCode)
        cursor.execute("update receiptsJournal,(select clientCode as cliCode, receiptDate as receiptDate, receipt as rct from receiptsJournal where receiptCode='%s') rj set beforeReceivable=beforeReceivable+rj.rct where clientCode=rj.cliCode and receiptsJournal.receiptDate>rj.receiptDate;" % receiptCode)
        cursor.execute("delete from receiptsJournal where receiptCode='%s';" % receiptCode)
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def update_historyReceivable(clientCode,historyReceivable,entryTime,entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("update receivableReport,clients set remainReceivable=remainReceivable-clients.historyReceivable+'%f', receivableReport.receivable=receivableReport.receivable-clients.historyReceivable+'%f', receivableReport.entryTime='%s', receivableReport.entryClerk='%s' where receivableReport.clientCode='%s' and receivableReport.clientCode=clients.clientCode;" % (historyReceivable, historyReceivable, entryTime, entryClerk, clientCode))
        cursor.execute("update clients set historyReceivable='%f', receivable=receivable-historyReceivable+'%f', entryTime='%s', entryClerk='%s' where clientCode='%s';" % (historyReceivable, historyReceivable, entryTime, entryClerk, clientCode))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

##### 付款 #####

# xijiawei
# 查询所有订单
def select_all_suppliers():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select supplierCode,historyPayable,payable,payment,payable-payment from suppliers;")
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_supplierByCode(supplierCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select supplier, address, contact, telephone  from suppliers where supplierCode='%s';" % supplierCode)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 模糊查询物料信息
def select_supplierInfoByFilter(filterStr):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select supplierCode from suppliers where supplierCode like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            lock.release()
            return result
        cursor.execute("select supplierCode from suppliers where supplier like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            lock.release()
            return result
        lock.release()
        return None
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_paymentsJournal(supplierCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select paymentCode,date_format(paymentDate,'%%Y-%%m-%%d'),beforePayable,payment,remark from paymentsJournal where supplierCode='%s';" % supplierCode)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_paymentsJournalSum(supplierCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select round(sum(payment),2) from paymentsJournal where supplierCode='%s' group by supplierCode;" % supplierCode)
        result = cursor.fetchall()
        lock.release()
        if result:
            return result[0][0]
        else:
            return 0
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有供应商应付款月度报表（暂不用）
def select_all_payableReport(month):
    try:
        suppliers = select_all_suppliers()
        result = []
        for i in suppliers:
            payable = select_payableReportByCode(i[0], month)
            result.append(payable[0])
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)

# xijiawei
# 查询所有订单
def select_payableReportByCode(supplierCode, month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select supplierCode,round(remainPayable,2),round(addPayable,2),round(payable,2),round(payment,2),remark from payableReport where supplierCode='%s' and month='%s';" % (supplierCode, month))
        result = cursor.fetchall()
        if not result:
            cursor.execute("select round(payable-payment,2) from payableReport where supplierCode='%s' and month in (select max(month) from payableReport where supplierCode='%s' and month<'%s');" % (supplierCode, supplierCode, month))
            remainPayableResult = cursor.fetchall()
            if remainPayableResult:
                remainPayable = remainPayableResult[0][0]
            else:
                cursor.execute("select historyPayable from suppliers where supplierCode='%s';" % (supplierCode))
                remainPayable = cursor.fetchall()[0][0]
            result=[[supplierCode,remainPayable,0,remainPayable,0,'']]
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_payableReportGroupByMaterialCodeByCode(supplierCode, month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select payableReportGroupByMaterialCode.supplierCode,payableReportGroupByMaterialCode.materialCode,materialType,materialNum,price,payable,payableReportGroupByMaterialCode.remark from payableReportGroupByMaterialCode,materialInfo where payableReportGroupByMaterialCode.supplierCode='%s' and month='%s' and payableReportGroupByMaterialCode.materialCode=materialInfo.materialCode;" % (supplierCode, month))
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_all_payableReportGroupByMaterialCode(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select payableReportGroupByMaterialCode.supplierCode,payableReportGroupByMaterialCode.materialCode,materialType,materialNum,price,payable,payableReportGroupByMaterialCode.remark from payableReportGroupByMaterialCode,materialInfo where month='%s' and payableReportGroupByMaterialCode.materialCode=materialInfo.materialCode;" % (month))
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def insert_paymentsJournal(supplierCode,paymentDate,beforePayable,payment,remark,entryTime,entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        paymentCode="R"+datetime.now().strftime('%Y%m%d%H%M%S%f')[0:16] # 使用时间戳生成唯一代号
        cursor.execute("insert into paymentsJournal (paymentCode,supplierCode,paymentDate,beforePayable,payment,remark,entryTime,entryClerk) values('%s','%s','%s','%f','%f','%s','%s','%s');"%(paymentCode,supplierCode,paymentDate,beforePayable,payment,remark,entryTime,entryClerk))
        cursor.execute("update suppliers set payment=payment+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s';" % (payment, entryTime, entryClerk, supplierCode))
        cursor.execute("update payableReport set payment=payment+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month='%s';" % (payment, entryTime, entryClerk, supplierCode, paymentDate[0:7]))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def delete_paymentsJournal(paymentCode):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("update payableReport,(select supplierCode as splCode, date_format(paymentDate,'%%Y-%%m') as month, payment as pmt from paymentsJournal where paymentCode='%s') pj set payment=payment-pj.pmt where supplierCode=pj.splCode and payableReport.month=pj.month;" % paymentCode)
        cursor.execute("update payableReport,(select supplierCode as splCode, date_format(paymentDate,'%%Y-%%m') as month, payment as pmt from paymentsJournal where paymentCode='%s') pj set remainPayable=remainPayable+pj.pmt, payable=payable+pj.pmt where supplierCode=pj.splCode and payableReport.month>pj.month;" % paymentCode)
        cursor.execute("update paymentsJournal,(select supplierCode as splCode, paymentDate as paymentDate, payment as pmt from paymentsJournal where paymentCode='%s') pj set beforePayable=beforePayable+pj.pmt where supplierCode=pj.splCode and paymentsJournal.paymentDate>pj.paymentDate;" % paymentCode)
        cursor.execute("delete from paymentsJournal where paymentCode='%s';" % paymentCode)
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def update_historyPayable(supplierCode,historyPayable,entryTime,entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("update payableReport,suppliers set remainPayable=remainPayable-suppliers.historyPayable+'%f', payableReport.payable=payableReport.payable-suppliers.historyPayable+'%f', payableReport.entryTime='%s', payableReport.entryClerk='%s' where payableReport.supplierCode='%s' and payableReport.supplierCode=suppliers.supplierCode;" % (historyPayable, historyPayable, entryTime, entryClerk, supplierCode))
        cursor.execute("update suppliers set historyPayable='%f', payable=payable-historyPayable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s';" % (historyPayable, historyPayable, entryTime, entryClerk, supplierCode))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

##### 工资 #####

# xijiawei
# 查询所有订单
def select_all_workerSalary():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select month, staff.staffid, name, position, workhours, overhours, timewage, piecewage, workagewage, subsidy, amerce, payablewage, tax, socialSecurityOfPersonal, otherdues, tax+socialSecurityOfPersonal+otherdues, realwage, socialSecurityOfEnterprise, salaryExpense  from staff,performance,workerSalary where staff.staffid=performance.staffid and staff.staffid=workerSalary.staffid order by staff.staffid;")
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_workerSalaryRecordByMonth(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select month, staff.staffid, name, position, workhours, overhours, timewage, piecewage, workagewage, subsidy, amerce, payablewage, tax, socialSecurityOfPersonal, otherdues, tax+socialSecurityOfPersonal+otherdues, realwage, socialSecurityOfEnterprise, salaryExpense  from staff,performance,workerSalaryRecord where staff.staffid=performance.staffid and staff.staffid=workerSalaryRecord.staffid and workerSalaryRecord.month='%s' order by staff.staffid;" % month)
        result = cursor.fetchall()
        # if not result:
        #     cursor.execute("select month, staff.staffid, name, position, workhours, overhours, timewage, piecewage, workagewage, subsidy, amerce, payablewage, tax, socialSecurityOfPersonal, otherdues, tax+socialSecurityOfPersonal+otherdues, realwage, socialSecurityOfEnterprise, salaryExpense  from staff,performance,workerSalary where staff.staffid=performance.staffid and staff.staffid=workerSalary.staffid order by staff.staffid;")
        #     result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def insert_workerSalary(month, name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("insert into staff (name, position, entryTime, entryClerk) values('%s','%s','%s','%s');" % (name, position, entryTime, entryClerk))
        cursor.execute("select max(staffid) from staff;")
        staffid = cursor.fetchall()[0][0]
        cursor.execute("insert into performance (staffid, workhours, overhours, entryTime, entryClerk) values('%d','%d','%d','%s','%s');" % (staffid, workhours, overhours, entryTime, entryClerk))
        cursor.execute("insert into workerSalary (staffid, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk) values('%d','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%s','%s');" % (staffid, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk))
        cursor.execute("insert into workerSalaryRecord (month, staffid, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk) values('%s','%d','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%s','%s');" % (month, staffid, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk))
        conn.commit()
        lock.release()
        return staffid
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def update_workerSalary(month, staffid, name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("update staff set name='%s', position='%s', entryTime='%s', entryClerk='%s' where staffid='%d';" % (name, position, entryTime, entryClerk, staffid))
        cursor.execute("update performance set workhours='%d', overhours='%d', entryTime='%s', entryClerk='%s' where staffid='%d';" % (workhours, overhours, entryTime, entryClerk, staffid))
        cursor.execute("update workerSalary set month='%s', realwage='%f', aftertaxwage='%f', payablewage='%f', salaryExpense='%f', timewage='%f', piecewage='%f', workagewage='%f', subsidy='%f', amerce='%f', tax='%f', socialSecurityOfPersonal='%f', otherdues='%f', socialSecurityOfEnterprise='%f', entryTime='%s', entryClerk='%s' where staffid='%d';" % (month, realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk, staffid))
        cursor.execute("update workerSalaryRecord set realwage='%f', aftertaxwage='%f', payablewage='%f', salaryExpense='%f', timewage='%f', piecewage='%f', workagewage='%f', subsidy='%f', amerce='%f', tax='%f', socialSecurityOfPersonal='%f', otherdues='%f', socialSecurityOfEnterprise='%f', entryTime='%s', entryClerk='%s' where staffid='%d' and month='%s';" % (realwage, aftertaxwage, payablewage, salaryExpense, timewage, piecewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk, staffid, month))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据id删除成员（暂不用）
def delete_staffByID(staffid):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("delete from staff where staffid='%d';"%staffid)
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据id删除成员（暂不用）
def delete_workerSalaryByIDAndMonth(staffid, month):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("delete from workerSalary where staffid='%d';"%staffid)
        cursor.execute("delete from workerSalaryRecord where staffid='%d' and month='%s';"%(staffid,month))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据id删除成员（暂不用）
def delete_managerSalaryByIDAndMonth(staffid, month):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("delete from managerSalary where staffid='%d';"%staffid)
        cursor.execute("delete from managerSalaryRecord where staffid='%d' and month='%s';"%(staffid,month))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_all_managerSalary():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select month, staff.staffid, name, position, workhours, overhours, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, payablewage, tax, socialSecurityOfPersonal, otherdues, tax+socialSecurityOfPersonal+otherdues, realwage, socialSecurityOfEnterprise, salaryExpense  from staff,performance,managerSalary where staff.staffid=performance.staffid and staff.staffid=managerSalary.staffid order by staff.staffid;")
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_managerSalaryRecordByMonth(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select month, staff.staffid, name, position, workhours, overhours, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, payablewage, tax, socialSecurityOfPersonal, otherdues, tax+socialSecurityOfPersonal+otherdues, realwage, socialSecurityOfEnterprise, salaryExpense  from staff,performance,managerSalaryRecord where staff.staffid=performance.staffid and staff.staffid=managerSalaryRecord.staffid and managerSalaryRecord.month='%s' order by staff.staffid;" % month)
        result = cursor.fetchall()
        # if not result:
        #     cursor.execute("select month, staff.staffid, name, position, workhours, overhours, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, payablewage, tax, socialSecurityOfPersonal, otherdues, tax+socialSecurityOfPersonal+otherdues, realwage, socialSecurityOfEnterprise, salaryExpense  from staff,performance,managerSalary where staff.staffid=performance.staffid and staff.staffid=managerSalary.staffid order by staff.staffid;")
        #     result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def insert_managerSalary(month, name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("insert into staff (name, position, entryTime, entryClerk) values('%s','%s','%s','%s');" % (name, position, entryTime, entryClerk))
        cursor.execute("select max(staffid) from staff;")
        staffid = cursor.fetchall()[0][0]
        cursor.execute("insert into performance (staffid, workhours, overhours, entryTime, entryClerk) values('%d','%d','%d','%s','%s');" % (staffid, workhours, overhours, entryTime, entryClerk))
        cursor.execute("insert into managerSalary (staffid, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk) values('%d','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%s','%s');" % (staffid, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk))
        cursor.execute("insert into managerSalaryRecord (month, staffid, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk) values('%s','%d','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%s','%s');" % (month, staffid, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk))
        conn.commit()
        lock.release()
        return staffid
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def update_managerSalary(month, staffid, name, position, workhours, overhours, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("update staff set name='%s', position='%s', entryTime='%s', entryClerk='%s' where staffid='%d';" % (name, position, entryTime, entryClerk, staffid))
        cursor.execute("update performance set workhours='%d', overhours='%d', entryTime='%s', entryClerk='%s' where staffid='%d';" % (workhours, overhours, entryTime, entryClerk, staffid))
        cursor.execute("update managerSalary set month='%s', realwage='%f', aftertaxwage='%f', payablewage='%f', salaryExpense='%f', basewage='%f', jobwage='%f', overtimewage='%f', performancewage='%f', workagewage='%f', subsidy='%f', amerce='%f', tax='%f', socialSecurityOfPersonal='%f', otherdues='%f', socialSecurityOfEnterprise='%f', entryTime='%s', entryClerk='%s' where staffid='%d';" % (month, realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk, staffid))
        cursor.execute("update managerSalaryRecord set realwage='%f', aftertaxwage='%f', payablewage='%f', salaryExpense='%f', basewage='%f', jobwage='%f', overtimewage='%f', performancewage='%f', workagewage='%f', subsidy='%f', amerce='%f', tax='%f', socialSecurityOfPersonal='%f', otherdues='%f', socialSecurityOfEnterprise='%f', entryTime='%s', entryClerk='%s' where staffid='%d' and month='%s';" % (realwage, aftertaxwage, payablewage, salaryExpense, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, tax, socialSecurityOfPersonal, otherdues, socialSecurityOfEnterprise, entryTime, entryClerk, staffid, month))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_workerSalaryByMonth(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select month, staff.staffid, name, position, workhours, overhours, timewage, piecewage, workagewage, subsidy, amerce, payablewage, tax, socialSecurityOfPersonal, otherdues, tax+socialSecurityOfPersonal+otherdues, realwage, socialSecurityOfEnterprise, salaryExpense  from staff,performance,workerSalaryRecord where month='%s' and staff.staffid=performance.staffid and staff.staffid=workerSalaryRecord.staffid order by staff.staffid;"%month)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_managerSalaryByMonth(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select month, staff.staffid, name, position, workhours, overhours, basewage, jobwage, overtimewage, performancewage, workagewage, subsidy, amerce, payablewage, tax, socialSecurityOfPersonal, otherdues, tax+socialSecurityOfPersonal+otherdues, realwage, socialSecurityOfEnterprise, salaryExpense  from staff,performance,managerSalaryRecord where month='%s' and staff.staffid=performance.staffid and staff.staffid=managerSalaryRecord.staffid order by staff.staffid;"%month)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_workerSalarySumByMonth(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select month from workerSalaryRecord where month='%s';" % month)
        if not cursor.fetchall():
            lock.release()
            return [[month, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        else:
            cursor.execute("select month, cast(round(sum(workhours),2) as signed), cast(round(sum(overhours),2) as signed), round(sum(timewage),2), round(sum(piecewage),2), round(sum(workagewage),2), round(sum(subsidy),2), round(sum(amerce),2), round(sum(payablewage),2), round(sum(tax),2), round(sum(socialSecurityOfPersonal),2), round(sum(otherdues),2), round(sum(tax+socialSecurityOfPersonal+otherdues),2), round(sum(realwage),2), round(sum(socialSecurityOfEnterprise),2), round(sum(salaryExpense),2)  from workerSalaryRecord, performance where month='%s' and workerSalaryRecord.staffid=performance.staffid;"%month)
            result = cursor.fetchall()
            lock.release()
            return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_managerSalarySumByMonth(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select month from managerSalaryRecord where month='%s';" % month)
        if not cursor.fetchall():
            lock.release()
            return [[month, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        else:
            cursor.execute("select month, cast(round(sum(workhours),2) as signed), cast(round(sum(overhours),2) as signed), round(sum(basewage),2), round(sum(jobwage),2), round(sum(overtimewage),2), round(sum(performancewage),2), round(sum(workagewage),2), round(sum(subsidy),2), round(sum(amerce),2), round(sum(payablewage),2), round(sum(tax),2), round(sum(socialSecurityOfPersonal),2), round(sum(otherdues),2), round(sum(tax+socialSecurityOfPersonal+otherdues),2), round(sum(realwage),2), round(sum(socialSecurityOfEnterprise),2), round(sum(salaryExpense),2)  from managerSalaryRecord, performance where month='%s' and managerSalaryRecord.staffid=performance.staffid;" % month)
            result = cursor.fetchall()
            lock.release()
            return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_workerSalarySumThisMonth():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        month = datetime.now().strftime('%Y-%m')
        cursor.execute("select cast(round(sum(workhours),2) as signed), cast(round(sum(overhours),2) as signed), round(sum(timewage),2), round(sum(piecewage),2), round(sum(workagewage),2), round(sum(subsidy),2), round(sum(amerce),2), round(sum(payablewage),2), round(sum(tax),2), round(sum(socialSecurityOfPersonal),2), round(sum(otherdues),2), round(sum(tax+socialSecurityOfPersonal+otherdues),2), round(sum(realwage),2), round(sum(socialSecurityOfEnterprise),2), round(sum(salaryExpense),2)  from workerSalary, performance where workerSalary.staffid=performance.staffid;")
        result = cursor.fetchall()
        lock.release()
        if not result[0][1]:
            return [[month, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        else:
            result_list = list(result[0])
            result_list.insert(0, month)
            return [result_list]
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_managerSalarySumThisMonth():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        month = datetime.now().strftime('%Y-%m')
        cursor.execute("select cast(round(sum(workhours),2) as signed), cast(round(sum(overhours),2) as signed), round(sum(basewage),2), round(sum(jobwage),2), round(sum(overtimewage),2), round(sum(performancewage),2), round(sum(workagewage),2), round(sum(subsidy),2), round(sum(amerce),2), round(sum(payablewage),2), round(sum(tax),2), round(sum(socialSecurityOfPersonal),2), round(sum(otherdues),2), round(sum(tax+socialSecurityOfPersonal+otherdues),2), round(sum(realwage),2), round(sum(socialSecurityOfEnterprise),2), round(sum(salaryExpense),2)  from managerSalary, performance where managerSalary.staffid=performance.staffid;")
        result = cursor.fetchall()
        lock.release()
        if not result[0][1]:
            return [[month, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        else:
            result_list = list(result[0])
            result_list.insert(0, month)
            return [result_list]
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

##### 其他费用之辅料 #####

# xijiawei
# 查询所有订单
def select_all_supplementarySuppliers():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select supplierCode from supplementarySuppliers;")
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 模糊查询物料信息
def select_supplementarySupplierInfoByFilter(filterStr):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select supplierCode from supplementarySuppliers where supplierCode like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            lock.release()
            return result
        cursor.execute("select supplierCode from supplementarySuppliers where supplier like '%%%s%%';" % (filterStr))
        result = cursor.fetchall()
        if result:
            print(result[0][0])
            lock.release()
            return result
        lock.release()
        return None
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_supplementaryByCode(supplierCode):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select supplierCode,supplementaryCode,date_format(inDate,'%%Y-%%m-%%d'),inNum,price,remark from supplementary where supplierCode='%s' order by inDate;"%supplierCode)
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_all_supplementary(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select supplierCode,date_format(inDate,'%%Y-%%m-%%d'),supplementaryCode,inNum,price,remark from supplementary where date_format(inDate,'%%Y-%%m')='%s' order by supplierCode;" % (month))
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_supplementaryByCodeAndMonth(supplierCode, month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select supplierCode,date_format(inDate,'%%Y-%%m-%%d'),supplementaryCode,inNum,price,remark from supplementary where supplierCode='%s' and date_format(inDate,'%%Y-%%m')='%s';" % (supplierCode, month))
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_supplementaryPayableReportByCode(supplierCode, month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select remark from supplementarySuppliers where supplierCode='%s';" % (supplierCode))
        result = cursor.fetchall()
        if result:
            remark = result[0][0]
        else:
            remark = ""
        cursor.execute("select supplierCode,round(remainPayable,2),round(addPayable,2),round(payable,2),round(payment,2) from supplementaryPayableReport where supplierCode='%s' and month='%s';" % (supplierCode, month))
        result = cursor.fetchall()
        if not result:
            cursor.execute("select round(payable-payment,2) from supplementaryPayableReport where supplierCode='%s' and month in (select max(month) from supplementaryPayableReport where supplierCode='%s' and month<'%s');" % (supplierCode, supplierCode, month))
            remainPayableResult = cursor.fetchall()
            if remainPayableResult:
                remainPayable = remainPayableResult[0][0]
            else:
                remainPayable = 0
            result=[[supplierCode,remainPayable,0,remainPayable,0,remark]]
        lock.release()
        return [[result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],remark]]
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def insert_supplementary(supplierCode,supplementaryCode,inDate,inNum,price,remark,entryTime,entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        inCode = "SP" + datetime.now().strftime('%Y%m%d%H%M%S%f')[0:16]  # 使用时间戳生成唯一代号
        cursor.execute("insert into supplementary (inCode, supplierCode,supplementaryCode,inDate,inNum,price,remark,entryTime,entryClerk) values('%s','%s','%s','%s','%d','%f','%s','%s','%s');"%(inCode, supplierCode,supplementaryCode,inDate,inNum,price,remark,entryTime,entryClerk))

        payable = price * inNum
        # 更新供应商的应付款
        cursor.execute("select supplierCode from supplementarySuppliers where supplierCode='%s';" % supplierCode)
        result = cursor.fetchall()
        if result:
            cursor.execute("update supplementarySuppliers set payable=payable+'%f', remark=concat(remark, '%s'), entryTime='%s', entryClerk='%s' where supplierCode='%s';" % (payable, remark, entryTime, entryClerk, supplierCode))
        else:
            cursor.execute("insert into supplementarySuppliers (supplierCode, supplier, payable, payment, remark, entryTime, entryClerk) values ('%s','%s','%f','%f','%s','%s','%s');" % (supplierCode, supplierCode, payable, 0, remark, entryTime, entryClerk))

        # 更新应付款报表
        month = inDate[0:7]
        cursor.execute("select supplierCode from supplementaryPayableReport where supplierCode='%s' and month='%s';" % (supplierCode, month))
        result = cursor.fetchall()
        if result:
            cursor.execute("update supplementaryPayableReport set addPayable=addPayable+'%f',payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month='%s';" % (payable, payable, entryTime, entryClerk, supplierCode, month)) # 更新该月的addPayable
            cursor.execute("update supplementaryPayableReport set remainPayable=remainPayable+'%f',payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month>'%s';" % (payable, payable, entryTime, entryClerk, supplierCode, month)) # 更新该月以后月份的remainPayable
        else:
            cursor.execute("select payable-payment from supplementaryPayableReport where supplierCode='%s' and month in (select max(month) from supplementaryPayableReport where supplierCode='%s' and month<'%s');" % (supplierCode, supplierCode, month))
            result = cursor.fetchall()
            if result:
                remainPayable = result[0][0]
            else:
                remainPayable = 0
            cursor.execute("insert into supplementaryPayableReport (supplierCode, month, remainPayable, addPayable, payable, payment, entryTime, entryClerk) value ('%s','%s','%f','%f','%f','%f','%s','%s');" % (supplierCode, month, remainPayable, payable, remainPayable + payable, 0, entryTime, entryClerk))

        # 更新应付款明细报表
        # cursor.execute("select supplierCode from supplementaryPayableReportGroupByMaterialCode where supplierCode='%s' and materialCode='%s' and month='%s';" % (supplierCode, supplementaryCode, month))
        # result = cursor.fetchall()
        # if result:
        #     cursor.execute("update payableReportGroupByMaterialCode set payable=payable+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and materialCode='%s' and month='%s';" % (payable, entryTime, entryClerk, supplierCode, supplementaryCode, month))
        # else:
        #     cursor.execute("insert into payableReportGroupByMaterialCode (supplierCode, materialCode, month, payable, entryTime, entryClerk) value ('%s','%s','%s','%f','%s','%s');" % (supplierCode, supplementaryCode, month, payable, entryTime, entryClerk))

        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def delete_supplementaryByCode(inCode, entryTime, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # 更新供应商的应付款
        cursor.execute("update supplementarySuppliers a,supplementary b set payable=payable-inNum*price, a.entryTime='%s', a.entryClerk='%s' where inCode='%s' and a.supplierCode=b.supplierCode;" % (entryTime, entryClerk, inCode))

        # 更新应付款报表
        month=entryTime[0:7]
        cursor.execute("update supplementaryPayableReport a,supplementary b set addPayable=addPayable-inNum*price,payable=payable-inNum*price, a.entryTime='%s', a.entryClerk='%s' where inCode='%s' and a.supplierCode=b.supplierCode and month=date_format(b.inDate,'%%Y-%%m');" % (entryTime, entryClerk, inCode)) # 更新该月的addPayable
        cursor.execute("update supplementaryPayableReport a,supplementary b set remainPayable=remainPayable-inNum*price,payable=payable-inNum*price, a.entryTime='%s', a.entryClerk='%s' where inCode='%s' and a.supplierCode=b.supplierCode and month>date_format(b.inDate,'%%Y-%%m');" % (entryTime, entryClerk, inCode)) # 更新该月以后月份的remainPayable

        # 删除
        cursor.execute("delete from supplementary where inCode='%s';"%(inCode))

        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def delete_supplementaryBySupplierCode(supplierCode, entryTime, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        # # 更新供应商的应付款
        # cursor.execute("update supplementarySuppliers,(select sum(inNum*price) as payableSum from supplementary where supplierCode='%s') t set payable=payable-t.payableSum, a.entryTime='%s', a.entryClerk='%s' where supplierCode='%s';" % (supplierCode, entryTime, entryClerk, supplierCode))
        # # 更新应付款报表
        # month=entryTime[0:7]
        # cursor.execute("update supplementaryPayableReport,(select sum(inNum*price) as payableSum from supplementary where supplierCode='%s') t set addPayable=addPayable-t.payableSum,payable=payable-t.payableSum, entryTime='%s', entryClerk='%s' where supplierCode='%s' and month='%s';" % (supplierCode, entryTime, entryClerk, supplierCode, month))
        # # 删除
        # cursor.execute("delete from supplementary where supplierCode='%s';"%(supplierCode))
        # conn.commit()

        cursor.execute("select inCode from supplementary where supplierCode='%s';"%supplierCode)
        result = cursor.fetchall()
        lock.release()
        for i in result:
            myThread(target=delete_supplementaryByCode, args=(i[0], entryTime, entryClerk,))
        lock.acquire()
        cursor.execute("delete from supplementarySuppliers where supplierCode='%s';" % supplierCode)
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def insert_supplementaryPayments(supplierCode, paymentDate, beforePayable, payment, remark, entryTime, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("insert into supplementaryPaymentsJournal (supplierCode,paymentDate,beforePayable,payment,remark,entryTime,entryClerk) values('%s','%s','%f','%f','%s','%s','%s');" % (supplierCode, paymentDate, beforePayable, payment, remark, entryTime, entryClerk))
        cursor.execute("update supplementarySuppliers set payment=payment+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s';" % (payment, entryTime, entryClerk, supplierCode))

        # 更新应付报表
        # cursor.execute("update supplementaryPayableReport set payment=payment+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month='%s';" % (payment, entryTime, entryClerk, supplierCode, paymentDate[0:7]))
        month = entryTime[0:7]
        cursor.execute("select supplierCode from supplementaryPayableReport where supplierCode='%s' and month='%s';" % (supplierCode, month))
        result = cursor.fetchall()
        if result:
            cursor.execute("update supplementaryPayableReport set payment=payment+'%f', entryTime='%s', entryClerk='%s' where supplierCode='%s' and month='%s';" % (payment, entryTime, entryClerk, supplierCode, paymentDate[0:7]))
        else:
            cursor.execute("select payable-payment from supplementaryPayableReport where supplierCode='%s' and month in (select max(month) from supplementaryPayableReport where supplierCode='%s' and month<'%s');" % (supplierCode, supplierCode, month))
            result = cursor.fetchall()
            if result:
                remainPayable = result[0][0]
            else:
                remainPayable = 0
            cursor.execute("insert into supplementaryPayableReport (supplierCode, month, remainPayable, addPayable, payable, payment, entryTime, entryClerk) value ('%s','%s','%f','%f','%f','%f','%s','%s');" % (supplierCode, month, remainPayable, 0, remainPayable, payment, entryTime, entryClerk))

        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

##### 其他费用之运营 #####

# xijiawei
# 查询所有运营费用（暂不用）
def select_all_operation():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select costCode, costDate, cost, remark, entryTime, entryClerk from operation;")
        result=cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_operationsByMonth(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select costCode, costDate, cost, remark, entryTime, entryClerk from operation where date_format(costDate,'%%Y-%%m')='%s' order by costCode;"%month)
        result=cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_operationSumByMonth(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select round(sum(cost),2) from operation where date_format(costDate,'%%Y-%%m')='%s';"%month)
        result = cursor.fetchall()[0][0]
        lock.release()
        if not result:
            return 0
        else:
            return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_operationSelect():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select distinct remark from operation;")
        result = cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_operationsBySelect(select, month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        if select=="-1":
            cursor.execute("select costCode, costDate, cost, remark, entryTime, entryClerk from operation where date_format(costDate,'%%Y-%%m')='%s' order by costCode;"%(month))
        else:
            cursor.execute("select costCode, costDate, cost, remark, entryTime, entryClerk from operation where remark='%s' and date_format(costDate,'%%Y-%%m')='%s' order by costCode;"%(select, month))
        result=cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_operationSumBySelect(select, month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        if select=="-1":
            cursor.execute("select round(sum(cost),2) from operation where date_format(costDate,'%%Y-%%m')='%s';"%(month))
        else:
            cursor.execute("select round(sum(cost),2) from operation where remark='%s' and date_format(costDate,'%%Y-%%m')='%s';"%(select, month))
        result = cursor.fetchall()[0][0]
        lock.release()
        if not result:
            return 0
        else:
            return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_operationsByDuration(select, startMonth, endMonth):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        if select=="-1":
            cursor.execute("select costCode, costDate, cost, remark, entryTime, entryClerk from operation where date_format(costDate,'%%Y-%%m')>='%s' and date_format(costDate,'%%Y-%%m')<='%s' order by costCode;"%(startMonth, endMonth))
        else:
            cursor.execute("select costCode, costDate, cost, remark, entryTime, entryClerk from operation where remark='%s' and date_format(costDate,'%%Y-%%m')>='%s' and date_format(costDate,'%%Y-%%m')<='%s' order by costCode;"%(select, startMonth, endMonth))
        result=cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_operationSumByDuration(select, startMonth, endMonth):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        if select=="-1":
            cursor.execute("select round(sum(cost),2) from operation where date_format(costDate,'%%Y-%%m')>='%s' and date_format(costDate,'%%Y-%%m')<='%s';"%(startMonth, endMonth))
        else:
            cursor.execute("select round(sum(cost),2) from operation where remark='%s' and date_format(costDate,'%%Y-%%m')>='%s' and date_format(costDate,'%%Y-%%m')<='%s';"%(select, startMonth, endMonth))
        result = cursor.fetchall()[0][0]
        lock.release()
        if not result:
            return 0
        else:
            return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 插入运营费用
def insert_operation(costDate, cost, remark, entryTime, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        costCode = "C" + datetime.now().strftime('%Y%m%d%H%M%S%f')[0:16]  # 使用时间戳生成唯一代号
        cursor.execute("insert into operation (costCode, costDate, cost, remark, entryTime, entryClerk) values('%s','%s','%f','%s','%s','%s');" % (costCode, costDate, cost, remark, entryTime, entryClerk))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据费用编号删除某项运营费用
def delete_operationByCode(costCode):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("delete from operation where costCode='%s';" % (costCode))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 更新运营费用
def update_operation(costCode, costDate, cost, remark, entryTime, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("update operation set costDate='%s', cost='%f', remark='%s', entryTime='%s', entryClerk='%s' where costCode='%s';" % (costDate, cost, remark, entryTime, entryClerk, costCode))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 删除某月所有运营费用（暂不用）
def delete_operationByMonth(month):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("delete from operation where date_format(costDate,'%%Y-%%m')='%s';" % (month))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

##### 其他费用之售后 #####

# xijiawei
# 查询所有售后费用（暂不用）
def select_all_aftersale():
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk from aftersale;")
        result=cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_aftersalesByMonth(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk from aftersale where date_format(costDate,'%%Y-%%m')='%s' order by costCode;"%month)
        result=cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_aftersaleSumByMonth(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select round(sum(laborCost),2), round(sum(materialCost),2), round(sum(otherCost),2) from aftersale where date_format(costDate,'%%Y-%%m')='%s';"%month)
        result = cursor.fetchall()[0]
        lock.release()
        if not result[0]:
            return [0,0,0]
        else:
            return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_aftersalesByDuration(startMonth, endMonth):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk from aftersale where date_format(costDate,'%%Y-%%m')>='%s' and date_format(costDate,'%%Y-%%m')<='%s' order by costCode;"%(startMonth, endMonth))
        result=cursor.fetchall()
        lock.release()
        return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_aftersaleSumByDuration(startMonth, endMonth):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select round(sum(laborCost),2), round(sum(materialCost),2), round(sum(otherCost),2) from aftersale where date_format(costDate,'%%Y-%%m')>='%s' and date_format(costDate,'%%Y-%%m')<='%s';"%(startMonth, endMonth))
        result = cursor.fetchall()[0]
        lock.release()
        if not result[0]:
            return [0,0,0]
        else:
            return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 插入售后费用
def insert_aftersale(costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        costCode = "C" + datetime.now().strftime('%Y%m%d%H%M%S%f')[0:16]  # 使用时间戳生成唯一代号
        cursor.execute("insert into aftersale (costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk) values('%s','%s','%s','%s','%f','%f','%f','%s','%s','%s','%s');" % (costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 根据费用编号删除某项售后费用
def delete_aftersaleByCode(costCode):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("delete from aftersale where costCode='%s';" % (costCode))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 更新售后费用
def update_aftersale(costCode, costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk):
    conn = dbpool.connect()
    cursor = conn.cursor()
    try:
        lock.acquire()
        cursor.execute("update aftersale set costDate='%s', productType='%s', client='%s', laborCost='%f', materialCost='%f', otherCost='%f', trackNumber='%s', remark='%s', entryTime='%s', entryClerk='%s' where costCode='%s';" % (costDate, productType, client, laborCost, materialCost, otherCost, trackNumber, remark, entryTime, entryClerk, costCode))
        conn.commit()
        lock.release()
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

##### 月度报表 #####

# xijiawei
# 查询所有订单
def select_addReceivableSumByMonth(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select round(sum(addReceivable),2) from receivableReport where month='%s';" % (month))
        result = cursor.fetchall()[0][0]
        lock.release()
        if not result:
            return 0
        else:
            return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_addPayableSumByMonth(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select round(sum(addPayable),2) from payableReport where month='%s';" % (month))
        result = cursor.fetchall()[0][0]
        lock.release()
        if not result:
            return 0
        else:
            return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()

# xijiawei
# 查询所有订单
def select_supplementaryAddPayableSumByMonth(month):
    try:
        lock.acquire()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("select round(sum(addPayable),2) from supplementaryPayableReport where month='%s';" % (month))
        result = cursor.fetchall()[0][0]
        lock.release()
        if not result:
            return 0
        else:
            return result
    except Exception as e:
        print("数据库操作异常：",e)
        current_app.logger.exception(e)
        conn.rollback()
