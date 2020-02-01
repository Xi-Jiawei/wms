import threading
import pymysql

import uuid
from datetime import datetime

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="test", charset="utf8")
cur = conn.cursor()

# xijiawei
# 同步锁
lock=threading.Lock()

def select(table, conf):
    sql = 'select * from ' + table + ' where 1 = 1'
    for item in conf:
        sql += item
    print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    return result

# 登录
def loginCheck(name, pwd):
    sql = "select * from authority where personName='%s' and password='%s'" % (name, pwd)
    conn.ping(reconnect=True)
    cur.execute(sql)
    result = cur.fetchall()
    if (len(result)) == 0:
        return False
    else:
        return True
    conn.close()

# 登录查询返回用户类型
def login_Authority(id):
    conn.ping(reconnect=True)
    sql = "select authority from  authority where personName='%s'" % (id)
    # sql = "select authority from  authority where personName='"+id+"';"
    cur.execute(sql)
    result = cur.fetchone()
    if result != None:
        for record in result:
            return record
    conn.close()

# 登录查询返回用户密码
def select_pwd(name):
    sql = "select password from  passwd where accountingid='%s'" % (name)
    cur.execute(sql)
    result = cur.fetchall()
    for record in result:
        return record
    conn.close()


# 修改用户密码
def update_pwd(name, pwd):
    sql = "update passwd set password= '%s'  where accountingid='%s'" % (pwd, name)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
    except:
        conn.rollback()

    conn.close()


# lh 管理员 增加用户
def db_add_account(id, name, pwd, gender, email, tel, introduce, ruletype):

    sql_account = "insert into account value ('%s','%s','%s','%s','%s','%s' ) " % (id, name, gender, email,tel,introduce)
    sql_pwd = "insert into passwd value ('%s','%s',%s)" % (id, pwd, ruletype)
    print(sql_account + " " + sql_pwd)
        # 执行SQL语句
    try:
        cur.execute(sql_account)
        cur.execute(sql_pwd)
        # 提交到数据库执行
        conn.commit()
        conn.close()
    except:
        conn.rollback()

# lh 管理员 查看全部人员返回所有结果
def show_allacount():
    sql = "select * from  account "
    cur.execute(sql)
    result = cur.fetchall()
    # for record in result:
    return result
    conn.close()


# cc 管理员_人员管理_查看人员
def show_allperson():
    sql = "select * from  authority "
    # print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    return result
    conn.close()


# cc 管理员增加人员
def cc_add_account(name, pwd, power):
    sql_account = "INSERT INTO authority (personName,password,authority) VALUES ('%s','%s','%s' ) " % (name, pwd, power)
    print(sql_account)
    # 执行SQL语句
    try:
        cur.execute(sql_account)
        # 提交到数据库执行
        conn.commit()
        result = cur.fetchall()
        return result
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()

# cc 管理员增加人员
def cc_findname():
    sql_find = 'SELECT personId,personName FROM authority'
    # 执行SQL语句
    try:
        cur.execute(sql_find)
        # 提交到数据库执行
        conn.commit()
        result = cur.fetchall()
        return result
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()

# cc 管理员删除人员
def cc_deletename(id):
    sql_delete = 'DELETE FROM authority WHERE personId = ' + id
    print(sql_delete)
    # 执行SQL语句
    try:
        cur.execute(sql_delete)
        # 提交到数据库执行
        conn.commit()
        result = cur.fetchall()
        return result
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()

# cc 修改人员权限
def cc_changeAuthority(id,authority):
    sql_change = 'UPDATE authority SET authority = \'' + authority + '\' WHERE personId ='+ id
    # print(sql_change)
    # 执行SQL语句
    try:
        cur.execute(sql_change)
        # 提交到数据库执行
        conn.commit()
        result = cur.fetchall()
        return result
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()

# cc 查询密码
def select_pass(name):
    sql = "select password from authority where personName='%s'" % (name)
    conn.ping(reconnect=True)
    cur.execute(sql)
    result = cur.fetchall()
    for record in result:
        return record
    conn.close()

# cc 修改用户密码
def update_pass(name, pwd):
    sql = "update authority set password= '%s'  where personName='%s'" % (pwd, name)
    print(sql)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        # print("语句已经提交")
    except:
        conn.rollback()
    conn.close()

# Bill学生打卡记录
def add_register(name):
    sql = "insert into register (accountingid,type,time) values(%s,%s,now())" % (name, 1)
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


# Bill 学生查看全部打卡记录返回所有结果
def show_register(name):
    sql = "select * from  register where accountingid='%s'" % (name)
    cur.execute(sql)
    result = cur.fetchall()
    # for record in result:
    return result
    conn.close()

# lh 学生查看全部课程
def show_allcourse():
    sql = "select * from  course "
    cur.execute(sql)
    result = cur.fetchall()
    # for record in result:
    return result
    conn.close()

# lh 学生查看全部已选课程
def show_allcoursesed(id):
    sql = "select course.courseid,course.coursename from courseselected ,course " \
          "where studentid='%s' and courseselected.courseid = course.courseid "  % (id)
    cur.execute(sql)
    result = cur.fetchall()
    # for record in result:
    return result
    conn.close()

# lh 学生选课
def dbstu_xuanke(courseid,stuid):
    print(courseid + " " + stuid)
    sql = "insert into courseselected  value('%s', '%s') " % (courseid,stuid)
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    conn.close()

# Bill 财务增加收支记录
def add_shouzhi(name,type,amount):
    sql = "insert into finance (accountingid,type,amount,time) values(%s,%s,%s,now())" % (name, type,amount)
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

# lh 财务 查看报表
def show_baobiao():
    sql = "select sum(f2.amount)/2 as shouru,sum(f1.amount)/2 as zhichu, (sum(f2.amount) - sum(f1.amount))/2  as shouzhi  " \
          "from  finance as f1,finance as f2 where f1.type = 1 and f2.type = 0"
    cur.execute(sql)
    result = cur.fetchall()
    # for record in result:
    return result
    conn.close()

# lh 财务 查看报表详细
def show_baobiaoxize():
    sql = "select  (CASE when type='0' then '收入' when type='1' then '支出' END)as type ,f.amount  from  finance f"
    cur.execute(sql)
    result = cur.fetchall()
    # for record in result:
    return result
    conn.close()


# Bill 老师增加课程
def add_course(course_id, course_name, teacher_name):
    sql = "insert into course (courseid,teacherid,coursename) values('%s','%s','%s' )" % (course_id, teacher_name, course_name)
    # print("sql语句: "+sql)
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

# lh 老师 查看课程
def show_allclass():
    sql = "select c.classid,stu.name from  class as c, account as stu where c.studentid = stu.accountingid"
    cur.execute(sql)
    result = cur.fetchall()
    # for record in result:
    return result
    conn.close()

# lh 老师 查看选课情况
def show_allcourseselected():
    sql = "SELECT rs.coursename, t.name, rs.stuname  " \
          "FROM (SELECT c.coursename , stu.name as stuname, c.teacherid FROM course as c, account as stu, " \
          "courseselected as cs   WHERE cs.courseid = c.courseid and cs.studentid = accountingid) as rs, account as t " \
          "where t.accountingid = rs.teacherid "
    cur.execute(sql)
    result = cur.fetchall()
    # for record in result:
    return result
    conn.close()

# lh 老师 查看考勤
def show_allregister():
    sql = "select a.name , r.time " \
          "from  register as r, account as a " \
          " where r.accountingid = a.accountingid"
    cur.execute(sql)
    result = cur.fetchall()
    # for record in result:
    return result
    conn.close()


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
    sql = "select materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost from materialsOfProduct where productCode='%s';"%(productCode)
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 根据多个成品编码汇总物料
def select_materialsOfProductByCodeArr(productCodeArr):
    length=len(productCodeArr)
    if length==0:
        return
    else:
        # sql="select m.materialCode,materialInfo.materialName,materialInfo.unit,materialInfo.inventoryNum,m.sum,materialInfo.inventoryNum-m.sum,materialInfo.supplier from (select materialInfo.materialCode,sum(materialsOfProduct.materialNum) sum from materialsOfProduct left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where materialsOfProduct.productCode='%s'"%productCodeArr[0]
        sql = "select m.materialCode,materialInfo.materialName,materialInfo.unit,materialInfo.inventoryNum,cast(m.sum as signed integer),cast(materialInfo.inventoryNum-m.sum as signed integer),materialInfo.supplier from (select materialInfo.materialCode,sum(materialsOfProduct.materialNum*productInfo.productNum) sum from materialsOfProduct left join productInfo on materialsOfProduct.productCode=productInfo.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where materialsOfProduct.productCode='%s'" % \
              productCodeArr[0]
        for productCode in productCodeArr[1:productCodeArr.__len__()]:
            sql+=" or materialsOfProduct.productCode='%s'"%productCode
        sql+=" group by materialInfo.materialCode) m,materialInfo where materialInfo.materialCode=m.materialCode;"
        print(sql)
    conn.ping(reconnect=True)
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

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
        #lock.release()
    finally:
        print("查询型号")

# xijiawei
# 根据成品编码查询成品其他成本组成信息
def select_otherCostsByCode(productCode):
    sql = "select processCost,adminstrationCost,supplementaryCost,operationCost,process, adminstration, supplementary, operation from otherCosts where productCode='%s';"%(productCode)
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

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
    sql = "select * from materialsOfProduct where productCode= '%s' and materialCode='%s';"% (productCode,materialCode)
    cur.execute(sql)
    result = cur.fetchall()
    return result
    conn.close()

# xijiawei
# 根据成品编码检查成品表
def check_productInfoByCode(productCode):
    sql = "select * from productInfo where productCode= '%s';"% (productCode)
    cur.execute(sql)
    result = cur.fetchall()
    return result
    conn.close()

# xijiawei
# 根据成品型号检查成品表
def check_productInfoByType(productType):
    sql = "select * from productInfo where productType= '%s';"% (productType)
    cur.execute(sql)
    result = cur.fetchall()
    return result
    conn.close()

# xijiawei
# 检查物料表
def check_materialInfo(materialCode):
    sql = "select * from materialInfo where materialCode= '%s';"% (materialCode)
    cur.execute(sql)
    result = cur.fetchall()
    return result
    conn.close()

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
    sql = "select p.productCode,productInfo.productType,p.productNum,p.client,p.remark,materialsOfProduct.materialCode,materialInfo.materialName,materialsOfProduct.materialNum from procurement p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s';"%(procurementCode)
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
    sql = "select materialInfo.materialCode,materialInfo.materialName,materialInfo.unit,materialInfo.inventoryNum+m.sum,m.sum,materialInfo.inventoryNum,materialInfo.supplier from materialInfo,(select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum) sum from procurement p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode) m where materialInfo.materialCode=m.materialCode;"%(procurementCode)
    try:
        cur.execute(sql)
        result = cur.fetchall()
        return result
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 取消采购
def delete_procurementByCode(procurementCode):
    try:
        # 更新materialInOut
        cur.execute("select materialInfo.materialCode,sum(materialsOfProduct.materialNum*p.productNum),materialInfo.unit,materialInfo.price,materialInfo.supplier from procurement p left join productInfo on p.productCode=productInfo.productCode left join materialsOfProduct on p.productCode=materialsOfProduct.productCode left join materialInfo on materialsOfProduct.materialCode=materialInfo.materialCode where p.procurementCode='%s' group by materialInfo.materialCode;" % (procurementCode))
        result = cur.fetchall()
        for i in result:
            # documentNumber = uuid.uuid1()  # 使用uuid生成唯一代号
            documentNumber=datetime.now().strftime('%Y%m%d%H%M%S%f') # 使用时间戳生成唯一代号
            documentNumber=documentNumber[0:16] # 使用时间戳生成唯一代号
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            insert_materialInOut(documentNumber, i[0], 0, i[1], i[2], i[3], i[4], entryTime, "系统账号")
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
            documentNumber=documentNumber[0:16] # 使用时间戳生成唯一代号
            entryTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            insert_materialInOut(documentNumber,i[0],1,i[1],i[2],i[3],i[4],entryTime,entryClerk)
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
# 根据物料编码查询物料信息
def select_materialInfoByCode(materialCode):
    sql = "select materialName,materialType,unit,inventoryNum,price,inventoryMoney,remark,supplier from materialInfo where materialCode='%s';"%materialCode
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

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
    # sql = "select materialInOut.materialCode,materialInfo.materialName,materialInfo.materialType,materialInOut.isInOrOut,materialInOut.beforeinventoryNum,materialInOut.operateNum,materialInOut.unit,materialInfo.price,materialInOut.operateNum*materialInfo.price,materialInOut.supplier,materialInOut.documentNumber,materialInOut.operateTime,materialInOut.operatorName from materialInOut left join materialInfo on materialInOut.materialCode=materialInfo.materialCode;"
    sql = "select m.materialCode,materialInfo.materialName,materialInfo.materialType,m.isInOrOut,m.beforeinventoryNum,m.operateNum,m.unit,m.price,m.operateNum*m.price,m.supplier,m.documentNumber,date_format(m.operateTime,'%Y-%m-%d %H:%i:%s'),m.operatorName from (select a.* from materialInOut a where 3>(select count(*) from materialInOut b where b.materialCode=a.materialCode and b.operateTime>a.operateTime)) m left join materialInfo on m.materialCode=materialInfo.materialCode order by m.materialCode,m.operateTime desc;"
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 根据时间段查询物料出入库记录
def select_all_materialInOutFilterByDate(startDate,endDate):
    sql = "select materialInOut.materialCode,materialInfo.materialName,materialInfo.materialType,materialInOut.isInOrOut,materialInOut.beforeinventoryNum,materialInOut.operateNum,materialInOut.unit,materialInOut.price,materialInOut.operateNum*materialInOut.price,materialInOut.supplier,materialInOut.documentNumber,date_format(materialInOut.operateTime,'%%Y-%%m-%%d %%H:%%i:%%S'),materialInOut.operatorName from materialInOut, materialInfo where materialInOut.materialCode=materialInfo.materialCode and materialInOut.operateTime>='%s' and materialInOut.operateTime<='%s' order by materialInOut.materialCode,materialInOut.operateTime desc;"%(startDate,endDate)
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
def insert_materialInOut(documentNumber,materialCode,isInOrOut,operateNum,unit,price,supplier,operateTime,operatorName):
    try:
        cur.execute("select inventoryNum from materialInfo where materialCode='%s';"%(materialCode))
        result = cur.fetchall()
        if result:
            sql = "insert into materialInOut (documentNumber,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplier,operateTime,operatorName)value('%s','%s','%d','%d','%d','%s','%d','%s','%s','%s');" \
                  % (documentNumber, materialCode, isInOrOut, result[0][0], operateNum, unit, price, supplier, operateTime,operatorName)
        else:
            sql = "insert into materialInOut (documentNumber,materialCode,isInOrOut,beforeinventoryNum,operateNum,unit,price,supplier,operateTime,operatorName)value('%s','%s','%d','%d','%d','%s','%d','%s','%s','%s');" \
                  % (documentNumber, materialCode, isInOrOut, 0, operateNum, unit, price, supplier, operateTime,operatorName)
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
def update_materialInOut(documentNumber, isInOrOut, operateNum, unit, price, supplier):
    try:
        cur.execute("select materialCode,isInOrOut,operateNum,operateTime from materialInOut where documentNumber='%s';" % (documentNumber))
        result = cur.fetchall()
        if result:
            materialCode=result[0][0]
            beforeIsInOrOut=result[0][1]
            beforeOperateNum=result[0][2]
            operateTime=result[0][3]
            if beforeIsInOrOut==0 and isInOrOut==0:
                cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % ((operateNum-beforeOperateNum),materialCode,operateTime))
                # 更新materialInfo表
                cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%d'*price where materialCode='%s';" % ((operateNum-beforeOperateNum), (operateNum-beforeOperateNum), materialCode))
            elif beforeIsInOrOut==1 and isInOrOut==0:
                cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % ((operateNum+beforeOperateNum),materialCode,operateTime))
                # 更新materialInfo表
                cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%d'*price where materialCode='%s';" % ((operateNum+beforeOperateNum), (operateNum+beforeOperateNum), materialCode))
            elif beforeIsInOrOut==0 and isInOrOut==1:
                cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum-'%d' where materialCode='%s' and operateTime>'%s';" % ((operateNum+beforeOperateNum),materialCode,operateTime))
                # 更新materialInfo表
                cur.execute("update materialInfo set inventoryNum=inventoryNum-'%d',inventoryMoney=inventoryMoney-'%d'*price where materialCode='%s';" % ((operateNum+beforeOperateNum), (operateNum+beforeOperateNum), materialCode))
            elif beforeIsInOrOut==1 and isInOrOut==1:
                cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum-'%d' where materialCode='%s' and operateTime>'%s';" % ((operateNum-beforeOperateNum),materialCode,operateTime))
                # 更新materialInfo表
                cur.execute("update materialInfo set inventoryNum=inventoryNum-'%d',inventoryMoney=inventoryMoney-'%d'*price where materialCode='%s';" % ((operateNum-beforeOperateNum), (operateNum-beforeOperateNum), materialCode))
        sql = "update materialInOut set isInOrOut='%d',operateNum='%d',unit='%s',price='%f',supplier='%s' where documentNumber='%s';" \
                  % (isInOrOut, operateNum, unit, price, supplier, documentNumber)
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
# 根据单据号删除物料出入库记录，更新相关物料出入库记录物料数量，并更新materialInfo表
def delete_materialInOutByDocNum(documentNumber):
    cur.execute("select materialCode,isInOrOut,operateNum,operateTime from materialInOut where documentNumber='%s';" % (documentNumber))
    result = cur.fetchall()
    if result:
        materialCode = result[0][0]
        isInOrOut = result[0][1]
        operateNum = result[0][2]
        operateTime=result[0][3]
    if isInOrOut == 0:
        cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum-'%d' where materialCode='%s' and operateTime>'%s';" % (operateNum, materialCode, operateTime))
        # 更新materialInfo表
        cur.execute("update materialInfo set inventoryNum=inventoryNum-'%d',inventoryMoney=inventoryMoney-'%d'*price where materialCode='%s';" % (operateNum, operateNum, materialCode))
    if isInOrOut == 1:
        cur.execute("update materialInOut set beforeinventoryNum=beforeinventoryNum+'%d' where materialCode='%s' and operateTime>'%s';" % (operateNum, materialCode, operateTime))
        # 更新materialInfo表
        cur.execute("update materialInfo set inventoryNum=inventoryNum+'%d',inventoryMoney=inventoryMoney+'%d'*price where materialCode='%s';" % (operateNum, operateNum, materialCode))
    # 删除记录
    sql = "delete from materialInOut where documentNumber='%s';" % (documentNumber)
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


# lh1  查看物料
def dao_show_material(materialCode, materialName, materialType, materialFactory):

    sql = 'select t1.materialCode,t1.materialName,t1.type,t1.department,t2.afterAmount,t2.afterMoney,' \
          't1.supplierFactory,t2.isInOrOut,t1.price,t2.amount,t2.totalPrice,t2.documentNumber,t2.time,t2.personName' \
          ' from materialOfInfo as t1 LEFT JOIN  materialOfInOut as t2  on t1.materialCode = t2.materialCode where 1=1 '
    if materialCode != '':
        sql += ' and t1.materialCode = \'' + materialCode + '\''
    if materialName != '':
        sql += ' and t1.materialName = \'' + materialName + '\''
    if materialType != '':
        sql += ' and t1.type = \'' + materialType + '\''
    if materialFactory != '':
        sql += ' and t1.supplierFactory =\'' + materialFactory + '\''
    print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    return result
    conn.close()

# lh1  查看物料物料静态表
def dao_show_materialinfo():
    conf = []
    result = select('materialOfInfo',conf)
    conn.ping(reconnect=True)
    return result
    conn.close()

# lh1  查看物料出入库信息
def dao_show_materialoutin():
    conf = []
    result = select('materialOfInOut',conf)
    return result
    conn.close()

# lh1  点击物料自动补全
def dao_show_materialoutorin(materialCode):
    conf = []
    if materialCode != '':
        conf.append(' and materialCode = \'' + materialCode + '\'')
    result = select('materialOfInfo',conf)
    return result
    conn.close()

# lh1  出库物料1
def dao_material_out(materialCode, materialName, materialType, m_price,materialFactory,mNum,mDepartment,mDcNum,materialTime,personName):
    # sql = "delete from materialOfInfo where materialName = '%s' "%( materialName )
    # print("sql语句: "+sql)
    # 更新余库存
    sql3 = " update materialOfInfo set remainderAmount = remainderAmount - '%d',remainderMoney = remainderMoney + '%lf'   where materialCode = '%s'" % (int(mNum), float(m_price) * int(mNum), materialCode)
    sql4 = "select * from materialOfInfo where materialCode = '%s' " % (materialCode)

    try:
        cur.execute(sql3)
        cur.execute(sql4)
        result = cur.fetchall()
        sql2 = "insert into materialOfInOut(personName,materialCode,materialName,type,amount,department,price,totalprice,documentNumber,supplierFactory, isInOrOut,time,afterAmount,afterMoney)" \
               " values('%s','%s','%s','%s', '%d','%s','%lf','%s','%s','%s',1,'%s','%d','%lf')" % \
               (personName, materialCode, materialName, materialType, int(mNum), mDepartment, float(m_price),
                float(m_price) * int(mNum), mDcNum, materialFactory, materialTime, result[0][5], result[0][6])
        cur.execute(sql2)
        conn.commit()
        return True
        conn.close()
    except:
        conn.rollback()

# lh1  入库物料0
def dao_material_in(materialCode, materialName, materialType, m_price,materialFactory,mNum,mDepartment,mDcNum,materialTime,personName):
    sql = "insert into materialOfInfo(materialCode,materialName,type,department,price,supplierFactory) " \
          "values('%s','%s','%s' ,'%s', '%lf', '%s')" % (materialCode, materialName, materialType, mDepartment, float(m_price), materialFactory)
    #更新静态表余库存
    sql3 = " update materialOfInfo set remainderAmount = remainderAmount + '%d',remainderMoney = remainderMoney + '%lf'   where materialName = '%s'" % (int(mNum), float(m_price) * int(mNum), materialName)
    sql4 = "select * from materialOfInfo where materialCode = '%s' " % (materialCode)
    res = cur.execute(sql4)

    try:
        if(res == 0):
            cur.execute(sql)
        cur.execute(sql3)
        cur.execute(sql4)
        result = cur.fetchall()
        if result:
            sql2 = "insert into materialOfInOut(personName,materialCode,materialName,type,amount,department,price,totalprice,documentNumber,supplierFactory, isInOrOut,time,afterAmount,afterMoney)" \
               " values('%s','%s','%s','%s', '%d','%s','%lf','%s','%s','%s',0,'%s','%d','%lf')" % \
               (personName, materialCode, materialName, materialType, int(mNum), mDepartment, float(m_price),
                float(m_price) * int(mNum), mDcNum, materialFactory, materialTime, result[0][5], result[0][6])
            cur.execute(sql2)
        conn.commit()
        return True
        conn.close()
    except:
        conn.rollback()


# lh1  修改物料
def dao_material_edit(materialCode, materialName, materialType, mDepartment,m_price,materialFactory,mCode):
    sql = "update materialOfInfo " \
          "set materialCode='%s',materialName='%s',type='%s',department ='%s', price ='%lf',supplierFactory='%s' where materialCode='%s'" \
          % (materialCode, materialName, materialType, mDepartment, float(m_price), materialFactory,mCode)
    sql2 = "update materialOfInOut " \
          "set materialCode='%s',materialName='%s',type='%s',department ='%s', price ='%lf',supplierFactory='%s' where materialCode='%s'" \
          % (materialCode, materialName, materialType, mDepartment, float(m_price), materialFactory, mCode)
    # print("sql语句: "+sql)
    try:
        cur.execute(sql)
        cur.execute(sql2)
        conn.commit()
        return True
        conn.close()
    except:
        conn.rollback()