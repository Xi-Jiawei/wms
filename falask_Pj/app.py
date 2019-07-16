from datetime import timedelta
from flask import Flask, url_for, render_template, request, redirect, session
from model import User, NewUser
from db import *
import config,datetime
import os

from form import MyForm, SelectForm, ChangeForm
from product_management import product_management

app = Flask(__name__)

# 静态文件缓存时间设置
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config.from_object(config)
app.config['SECRET_KEY'] = os.urandom(24)  # 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。


# app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=7) #设置session的保存时间。

# 首页 根据passwd里面的Authority展示对应的主页
# 1-管理员
# 2-老师
# 3-财务人员
# 4-学生
# @app.route('/')
# def index():
#     return render_template('index.html')



# bill学生主页
@app.route('/stu_index')
def index_stu():
    return render_template('stu_index.html')

# bill教师主页
@app.route('/teacher_index')
def index_teacher():
    return render_template('teacher_index.html')

# Bill 老师添加课程信息
@app.route('/add_class', methods=['GET', 'POST'])
def add_class():
    print("添加课程界面", session['username'])
    if request.method == "POST":
        user = User()
        user.name = session['username']
        course_id = request.form["course_id"]
        course_name = request.form["course_name"]
        teacher_name = request.form["teacher_name"]
        print("执行添加收支的课程是", course_name)
        print("教师名称", teacher_name)
        if add_course(course_id, course_name, teacher_name):
            print("课程增加成功")
            message = "课程增加成功"
            return render_template('teacher_addclass.html', message=message)
        else:
            message = "课程增加失败,请重新填写"
            print("课程增加失败,请重新填写")
            return render_template('teacher_addclass.html', message=message)
            #   session.pop(user.name)
    else:
        return render_template('teacher_addclass.html')

# lh 老师 查看班级信息
@app.route('/show_class', methods=['GET', 'POST'])
def show_class():
    # print("课程查询界面", session['username'])
    allclass = show_allclass()
    print(allclass)
    return render_template('teacher_showclass.html', allclass=allclass)

# lh 老师 查看选课信息
@app.route('/show_csselect', methods=['GET', 'POST'])
def show_allcourseofselect():
    # print("课程查询界面", session['username'])
    allselected = show_allcourseselected()
    print(allselected)
    return render_template('teacher_showcsselected.html', allselected=allselected)

# lh 老师 查看选课信息
@app.route('/show_register', methods=['GET', 'POST'])
def show_register():
    # print("课程查询界面", session['username'])
    allregister = show_allregister()
    print(allregister)
    return render_template('teacher_showregister.html', allregister=allregister)


# bill财务人员主页
@app.route('/account_index')
def index_account():
    return render_template('account_index.html')


# bill管理员
@app.route('/admin')
def index_adm():
    return render_template('adm_index.html')

# cc 操作员
@app.route('/oprator')
def index_operator():
    print(session['username'])
    return render_template('operator_index.html')

# cc 登陆
@app.route('/login/', methods=['GET', 'POST'])
def user_login():
    print(session)
    if session:
        username = session['username']
        # session.pop('username')
        print('session 不为空 ', username)
        print("开始调用函数获取用户类型")
        Authority = login_Authority(username)
        print("Authority", Authority)
        if Authority == '888':
            print("admin login!")
            return redirect(url_for('index_adm'))
        else:
            print("oprator login!")
            return redirect(url_for('index_operator'))

    # print(session[0])
    if request.method == "POST":
        print(request.form)
        user = User()
        stu_id = user.id = request.form["user_id"]
        user.pwd = request.form["user_pwd"]
        Authority = login_Authority(user.id)
        print("测试Authorith 输出数字", Authority)
        # print("admin login", Authority)
        # print(type(Authority))
        if loginCheck(user.id, user.pwd):
            session['username'] = user.id
            if Authority == '888':
                print("admin login!")
                return redirect(url_for('index_adm'))
            else:
                print("oprator login!")
                return redirect(url_for('index_operator'))
        else:
            message = "用户名或者密码错误"
            return render_template('user_login.html', message=message)
        print("name:  pwd:", user.name, user.pwd)
        return redirect(url_for("user_login"))  # 跳到主页
    return render_template('user_login.html')


# bill退出系统
@app.route('/out', methods=['GET', 'POST'])
def out():
    session.pop('username')
    return redirect(url_for('user_login'))


# bill修改密码
@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    print("修改界面", session['username'])
    # sql 修改数据库中的密码
    # fun_changepassword(user)
    if request.method == "POST":
        user = User()
        user.name = session['username']
        print("需要修改的用户是", user.name)
        user.pwd = select_pwd(user.name)
        print("数据库查询到的密码是：", user.pwd)
        oldpassword = request.form["oldpassword"]
        print("需要修改的用户是", oldpassword)
        newpassword = request.form["newpassword"]
        renewpassword = request.form["renewpassword"]
        if newpassword == renewpassword:
            print("两次输入密码一致")
            print("----------------------------------------------")
        else:
            message = "两次密码不一致，请重新输入"
            print("两次密码不一致，请重新输入")
            return render_template('changepassword.html', message=message)
        # print("新密码： 旧密码：", oldpassword, user.pwd[0])
        if str(oldpassword) == str(user.pwd[0]):
            print("新旧密码一致")
            user.pwd = newpassword
            update_pwd(user.name, user.pwd)
            print("密码修改成功")
            print("密码修改成功，请推出当前界面重新登陆")
            # return 'ok'
            message = "密码修改成功，请重新登陆"
            # session.pop(user.name)
            return redirect(url_for("user_login"))  # 跳到主页
            # return render_template('user_login.html', message=message)
        else:
            message = "旧密码有误，请重新输入"
            print("旧密码有误，请重新输入")
            return render_template('changepassword.html', message=message)
            #   session.pop(user.name)
    else:
        return render_template('changepassword.html')

# lh 管理员 增加人员
@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if request.method == "POST":
        print("增加人员: ")
        user = User()
        user.id = request.form["accountid"]
        user.name = request.form["name"]
        user.pwd = request.form["pwd"]
        user.gender = request.form["gender"]
        user.email = request.form["email"]
        user.tel = request.form["tel"]
        user.introduce = request.form["introduce"]
        user.ruletype = request.form["ruletype"]
        db_add_account(user.id, user.name, user.pwd, user.gender, user.email, user.tel, user.introduce, user.ruletype)
        add_message = "添加成功"
        return render_template('adm_add_account.html',add_message = add_message)
    return render_template('adm_add_account.html')

# lh 管理员 查看人员
@app.route('/show_account')
def show_account():
    # print("查看人员: ")
    # sql 查看人员数据库中的所有人员
    account = show_allacount()
    # print(account)
    return render_template('adm_show_account.html',account =account)

# cc 管理员 人员管理
@app.route('/person_management',methods=['GET', 'POST'])
def person_management():
    return render_template('person_management.html')

# cc 人员管理_查看人员
@app.route('/show_person',methods=['GET', 'POST'])
def show_person():
    person = show_allperson()
    # print(person)
    return render_template('person_management_show.html',person =person)

# cc 人员管理_增加人员
@app.route('/add_person',methods=['GET', 'POST'])
def add_person():
    form = MyForm()
    if request.method == "POST":
        # print(form.data['status'])
        # print(form.data['statusPro'])
        # print(form.data['statusPur'])
        print("增加人员: ")
        user = NewUser()
        user.name = request.form["name"]
        authority = form.data['status'] + "" + form.data['statusPro'] + "" + form.data['statusPur']
        user.authority = authority
        print(user.name, user.pwd, user.authority)
        cc_add_account(user.name, user.pwd, user.authority)
        add_message = "添加成功"
        return render_template('add_person.html', add_message=add_message, form=form)
    return render_template('add_person.html',form=form)

# cc 人员管理_删除人员
@app.route('/delete_person',methods=['GET', 'POST'])
def delete_person():
    result = cc_findname()
    person = show_allperson()
    form = SelectForm()
    if request.method == "POST":
        print("删除人员: ")
        id = form.data['personName']
        cc_deletename(id)
        delete_message = "删除成功"
        return render_template('delete_person.html', delete_message=delete_message, form=form, person=person)
    return render_template('delete_person.html', form=form, person=person)

# cc 人员管理_权限管理
@app.route('/change_person',methods=['GET', 'POST'])
def change_person():
    person = show_allperson()
    form = ChangeForm()
    if request.method == "POST":
        print("修改人员权限")
        id = form.data['personName']
        authority = form.data['status'] + "" + form.data['statusPro'] + "" + form.data['statusPur']
        cc_changeAuthority(id,authority)
        change_message = "修改成功"
        return render_template('change_person.html', change_message=change_message, form=form, person=person)
    return render_template('change_person.html', form=form, person=person)
# Bill  学生签到
@app.route('/stu_register', methods=['GET', 'POST'])
def stu_register():
    print("签到界面", session['username'])
    if request.method == "POST":
        user = User()
        user.name = session['username']
        print("需要签到的用户是", user.name)
        if add_register(user.name):
            print("签到成功")
            message = "签到成功"
            return render_template('stu_register.html', message=message)
        else:
            message = "签到成功,请重新打卡"
            print("签到成功,请重新打卡")
            return render_template('stu_register.html', message=message)
            #   session.pop(user.name)
    else:
        return render_template('stu_register.html')

# lh 学生选课
@app.route('/stu_xuanke', methods=['GET', 'POST'])
def stu_xuanke():
    all_course = show_allcourse()
    stu_id = session['username']
    all_coursesed = show_allcoursesed(stu_id)
    if request.method == "POST":
        print(request.form)
        courseid = request.form["course_id"]
        dbstu_xuanke(courseid,stu_id)
    return render_template('stu_xuanke.html',all_course = all_course,all_coursesed = all_coursesed)

# Bill 财务人员 增加收支记录
@app.route('/accounting_shouzhi', methods=['GET', 'POST'])
def accounting_shouzhi():
    print("添加收支界面", session['username'])
    if request.method == "POST":
        user = User()
        user.name = session['username']
        add_type = request.form["add_type"]
        amount = request.form["add_amount"]
        print("执行添加收支的金额是", amount)
        print("执行添加收支的用户是", user.name)
        if add_shouzhi(user.name, add_type, amount):
            print("收支增加成功")
            message = "收支增加成功"
            return render_template('accounting_shouzhi.html', message=message)
        else:
            message = "收支增加失败,请重新填写"
            print("收支增加失败,请重新填写")
            return render_template('accounting_shouzhi.html', message=message)
            #   session.pop(user.name)
    else:
        return render_template('accounting_shouzhi.html')

# lh 财务 查看报表统计
@app.route('/accounting_baobiao', methods=['GET', 'POST'])
def accounting_baobiao():
    # print("课程查询界面", session['username'])
    baobiao = show_baobiao()
    baobiaoxize = show_baobiaoxize();
    print(baobiaoxize)
    return render_template('accounting_baobiao.html', baobiao=baobiao,baobiaoxize = baobiaoxize)


# lh 查看物料信息
@app.route('/show_material', methods=['GET', 'POST'])
def show_material():
    materialCode = ''
    materialName = ''
    materialTime = ''
    materialType = ''
    materialFactory = ''
    personName = session['username']
    if request.method == "POST":
        materialCode = request.form["materialCode"]
        materialName = request.form["materialName"]
        materialTime = request.form["materialTime"]
        materialType = request.form["materialType"]
        materialFactory = request.form["materialFactory"]
    materialAll = dao_show_material(materialCode, materialName, materialTime, materialType, materialFactory)
    materialinfoAll = dao_show_materialinfo()
    materialoutinAll = dao_show_materialoutin()
    # print(materialAll)
    return render_template('material_index.html', materialAll=materialAll, materialCode=materialCode,
                           materialName=materialName, materialTime=materialTime, materialType=materialType,
                           materialFactory=materialFactory)
# lh 物料出入库
@app.route('/material_outorin/<mName>', methods=['GET', 'POST'])
def material_outorin(mName):
    # print("出入库传参"+mName)
    material_init = dao_show_materialoutorin(mName)
    materialCode = ''
    materialName = ''
    materialType = ''
    materialFactory = ''
    materialTime = datetime.datetime.today()

    personName = session['username']
    mNum = ''
    mDepartment = ''
    m_price = 0
    mDcNum = ''
    isinorout = -1
    if request.method == "POST":
        materialCode = request.form["materialCode"]
        materialName = request.form["materialName"]
        materialType = request.form["materialType"]
        materialFactory = request.form["materialFactory"]

        mNum = request.form['mNum']
        mDepartment = request.form['mDepartment']
        m_price = request.form['m_price']
        mDcNum = request.form['mDcNum']
        isinorout = request.form['isinorout']
        print("物料出入库", session['username'],isinorout)
        if isinorout == '1':
           print("出库！")
           if dao_material_out(materialName):
                print("出库成功")
                message = "出库成功"
                return render_template('material_outorin.html', message=message)
           else:
                message = "出库失败,请重新填写"
                print("出库失败,请重新填写")
                return render_template('material_outorin.html', message=message)
                #   session.pop(user.name)
        else:
            print("入库！")
            materialCode = request.form["materialCode"]
            materialName = request.form["materialName"]
            materialType = request.form["materialType"]
            materialFactory = request.form["materialFactory"]

            mNum = request.form['mNum']
            mDepartment = request.form['mDepartment']
            m_price = request.form['m_price']
            mDcNum = request.form['mDcNum']
            isinorout = request.form['isinorout']
            if dao_material_in(materialCode, materialName, materialType, m_price,materialFactory,mNum,mDepartment,mDcNum,materialTime,personName):
                print("入库成功")
                message = "入库成功"
                return render_template('material_outorin.html', message=message)
            else:
                message = "入库失败,请重新填写"
                print("入库失败,请重新填写")
                return render_template('material_outorin.html', message=message)
                #   session.pop(user.name)
    else:
        for i in material_init:
            materialCode = i[0]
            materialName = i[1]
            materialType = i[2]
            materialFactory = i[8]
            mDepartment = i[3]
            m_price = i[4]
        print("materialFactory:" + materialFactory)
        return render_template('material_outorin.html',materialCode=materialCode,materialName=materialName,
                               materialType=materialType,mDepartment=mDepartment,m_price=m_price,materialFactory=materialFactory)

# xijiawei
# 添加“product_management.py”蓝本
app.register_blueprint(product_management)


if __name__ == '__main__':
    app.run(debug=True)