import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="test", charset="utf8")
cur = conn.cursor()

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
    sql = "select productCode,productType,client,price,profit from productInfo;"
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 查询成品录入信息
def select_productChangeByCode(productCode):
    sql = "select entryClerk,updateOfContent,isUpdateOrAdd,entryDate from productChange where productCode='%s';" % (productCode)
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 查询成品信息
def select_productInfoByCode(productCode):
    sql = "select productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost from productInfo where productCode='%s';"%(productCode)
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 查询成品物料组成
def select_materialsOfProductByCode(productCode):
    sql = "select materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost from materialsOfProduct where productCode='%s';"%(productCode)
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 查询成品其他成本组成信息
def select_otherCostsByCode(productCode):
    sql = "select project,procCost,adminCost,suppleCost,operaCost from otherCosts where productCode='%s';"%(productCode)
    cur.execute(sql)
    result=cur.fetchall()
    return result
    conn.close()

# xijiawei
# 插入成品静态表
def insert_productInfo(productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost):
    sql = "insert into productInfo (productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost)value('%s','%s','%s','%f','%f','%f','%f','%f','%f','%f','%f','%f');" \
          % (productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost)
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
# 插入成品物料组成表
def insert_materialsOfProduct(productCode,materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost):
    sql = "insert into materialsOfProduct (productCode,materialCode,materialNum,materialPrice,materialCost,patchPoint,patchPrice,patchCost)value('%s','%s','%d','%f','%f','%d','%f','%f');" \
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
# 插入成品费用组成表
def insert_otherCosts(productCode,project,procCost,adminCost,suppleCost,operaCost):
    sql = "insert into otherCosts (productCode,project,procCost,adminCost,suppleCost,operaCost)value('%s','%s','%f','%f','%f','%f');" \
          % (productCode,project,procCost,adminCost,suppleCost,operaCost)
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
# 插入成品录入表
def insert_productChange(productCode,entryClerk,updateOfContent,entryDate):
    # entryDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    sql = "insert into productChange (productCode,entryClerk,updateOfContent,entryDate)value('%s','%s','%s','%s');" \
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
# 更新成品物料组成表
def update_productInfo(productCode,productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost):
    sql = "update productInfo set productType='%s',client='%s',price='%f',profit='%f',totalCost='%f',taxRate='%f',materialCost='%f',processCost='%f',adminstrationCost='%f',supplementaryCost='%f',operatingCost='%f' where productCode='%s';" \
          % (productType,client,price,profit,totalCost,taxRate,materialCost,processCost,adminstrationCost,supplementaryCost,operatingCost,productCode)
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
# 更新成品物料组成表
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
# 更新成品物料组成表
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
# 更新成品物料组成表
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
# 更新成品物料组成表
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
# 检查成品表
def check_productInfo(productCode):
    sql = "select * from productInfo where productCode= '%s';"% (productCode)
    cur.execute(sql)
    result = cur.fetchall()
    return result
    conn.close()

# xijiawei
# 检查物料表
def check_materialOfInfo(materialCode):
    sql = "select * from materialOfInfo where materialCode= '%s';"% (materialCode)
    cur.execute(sql)
    result = cur.fetchall()
    return result
    conn.close()

# xijiawei
# 插入成品录入表
def insert_materialOfInfo(materialCode, price, remainderAmount, supplierFactory):
    # entryDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    sql = "insert into materialOfInfo (materialCode, price, remainderAmount, supplierFactory)value('%s','%f','%d','%s');" \
          % (materialCode, price, remainderAmount, supplierFactory)
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
# 查询物料表
def select_materialOfInfo(materialCode):
    sql = "select materialCode, price, remainderAmount, supplierFactory from materialOfInfo where materialCode= '%s';"% (materialCode)
    try:
        cur.execute(sql)
        result = cur.fetchall()
        return result
        conn.close()
    except:
        conn.rollback()

# xijiawei
# 创建物料组成临时表
def create_materialsOfProduct_temp():
    sql = "create table if not exists materialsOfProduct_temp(" \
          "id int," \
          "materialCode varchar(50) not null primary key);"
    try:
        cur.execute("drop table if exists materialsOfProduct_temp;")
        conn.commit()

        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("语句已经提交")
        return True
        conn.close()
    except:
        conn.rollback()

# # xijiawei
# # 检查物料组成临时表
# def check_materialsOfProduct_temp(id):
#     sql = "select * from materialsOfProduct_temp where id= '%s=d';"% (id)
#     cur.execute(sql)
#     result = cur.fetchall()
#     return result
#     conn.close()
#
# # xijiawei
# # 检查物料组成临时表
# def check_materialsOfProduct_temp(id,materialCode):
#     sql = "select * from materialsOfProduct_temp where id='%d' materialCode= '%s';"% (id,materialCode)
#     cur.execute(sql)
#     result = cur.fetchall()
#     return result
#     conn.close()

# # xijiawei
# # 检查物料组成临时表
# def check_materialsOfProduct_temp(*param):
#     print(param)
#     print(len(param))
#     if len(param) == 1:
#         print("参数个数为1：%s" % (param[0]))
#         sql = "select * from materialsOfProduct_temp where id= '%d';" % (param[0])
#     elif len(param) == 2:
#         print("参数个数为1：%s; %s" % (param[0], param[1]))
#         sql = "select * from materialsOfProduct_temp where not id='%d' and materialCode= '%s';" % (
#             param[0], param[1])
#     cur.execute(sql)
#     result = cur.fetchall()
#     return result
#     conn.close()

# xijiawei
# 检查物料组成临时表
def check_materialsOfProduct_temp1(id):
    print("1")
    #conn.ping(reconnect=True)
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="test", charset="utf8")
    #sql = 'select * from materialsOfProduct_temp'
    conn.ping(reconnect=True)
    cur = conn.cursor()

    try:
        sql = "select * from materialsOfProduct_temp where id= '%d';" % (id)
        print(sql)
        cur.execute(sql)
        result = cur.fetchall()
        return result
        # conn.close()
    except:
        print("出错1")
        conn.rollback()

# xijiawei
# 检查物料组成临时表
def check_materialsOfProduct_temp2(id,materialCode):
    print("2")

    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="test", charset="utf8")
    #sql = 'select * from materialsOfProduct_temp'
    conn.ping(reconnect=True)
    cur = conn.cursor()
    #cur.execute(sql)
    #conn.commit()

    try:
        sql = "select * from materialsOfProduct_temp where not(id='%d') and materialCode= '%s';" % (id, materialCode)
        print(sql)
        cur.execute(sql)
        result = cur.fetchall()
        return result
        # conn.close()
    except:
        print("出错2")
        conn.rollback()

# xijiawei
# 插入物料组成临时表
def insert_materialsOfProduct_temp(id,materialCode):
    sql = "insert into materialsOfProduct_temp (id,materialCode) value('%d','%s');"% (id,materialCode)
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
# 插入物料组成临时表
def update_materialsOfProduct_temp(id,materialCode):
    sql = "update materialsOfProduct_temp set materialCode='%s' where id='%d';"% (materialCode,id)
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
def dao_show_material(materialCode, materialName, materialTime, materialType, materialFactory):
    conf = []
    # if materialTime == '':
    #     conf.append(' and DATE_FORMAT(BehaviorTime,\'%Y%m%d\') >= \'20180102\'')
    # else:
    #     conf.append(' and DATE_FORMAT(BehaviorTime,\'%Y%m%d\') >= \'' + materialName + '\'')
    if materialCode != '':
        conf.append(' and materialCode = \'' + materialCode + '\'')
    if materialName != '':
        conf.append(' and materialName = \'' + materialName + '\'')
    if materialType != '':
        conf.append(' and type = ' + materialType)
    if materialFactory != '':
        conf.append(' and supplierFactory =\'' + materialFactory + '\'')

    sql = 'select t1.materialCode,t1.materialName,t1.type,t1.department,t1.remainderAmount,t1.remainderMoney,' \
          't1.supplierFactory,t2.isInOrOut,t1.price,t2.amount,t2.totalPrice,t2.documentNumber,t2.time,t2.personName' \
          ' from materialofinfo as t1 INNER JOIN  materialofinout as t2  on t1.materialName = t2.materialName '
    cur.execute(sql)
    result = cur.fetchall()
    return result
    conn.close()

# lh1  查看物料物料静态表
def dao_show_materialinfo():
    conf = []
    result = select('materialofinfo',conf)
    return result
    conn.close()

# lh1  查看物料出入库信息
def dao_show_materialoutin():
    conf = []
    result = select('materialofinout',conf)
    return result
    conn.close()

# lh1  点击物料自动补全
def dao_show_materialoutorin(materialName):
    conf = []
    if materialName != '':
        conf.append(' and materialName = \'' + materialName + '\'')
    result = select('materialofinfo',conf)
    return result
    conn.close()

# lh1  出库物料
def dao_material_out(materialName):
    sql = "delete from materialofinfo where materialName = '%s' "%( materialName )
    # print("sql语句: "+sql)
    sql2 = "delete from materialofinout where materialName = '%s' " %( materialName )
    # print("sql语句: " + sql2)
    try:
        cur.execute(sql)
        cur.execute(sql2)
        conn.commit()
        return True
        conn.close()
    except:
        conn.rollback()

# lh1  入库物料
def dao_material_in(materialCode, materialName, materialType, m_price,materialFactory,mNum,mDepartment,mDcNum,materialTime,personName):
    sql = "insert into materialofinfo(materialCode,materialName,type,department,price,supplierFactory) " \
          "values('%s','%s','%s' ,'%s', '%lf', '%s')" % (materialCode, materialName, materialType, mDepartment, float(m_price), materialFactory)
    # print("sql语句: "+sql)
    sql2 = "insert into materialofinout(personName,materialCode,materialName,type,amount,department,price,totalprice,documentNumber,supplierFactory, isInOrOut,time)" \
           " values('%s','%s','%s','%s', '%d','%s','%lf','%s','%s','%s',0,'%s')" % \
           (personName,materialCode, materialName, materialType, int(mNum), mDepartment, float(m_price),float(m_price)*int(mNum), mDcNum, materialFactory,materialTime)
    #更新余库存
    sql3 = " update materialofinfo set remainderAmount = remainderAmount + '%d',remainderMoney = remainderMoney + '%lf'   where materialName = '%s'" % (int(mNum), float(m_price) * int(mNum), materialName)

    sql4 = "select * from materialofinfo where materialName = '%s' " % (materialName)
    print("sql4语句: " + sql4)
    res = cur.execute(sql4)
    print(res)
    try:
        if(res == 0):
            cur.execute(sql)
        cur.execute(sql2)
        cur.execute(sql3)
        conn.commit()
        return True
        conn.close()
    except:
        conn.rollback()