from datetime import timedelta

from flask import Flask, url_for, render_template, request, redirect, session

from model import User, NewUser
from db import *
import config,datetime
import os
import sys

from form import MyForm, SelectForm, ChangeForm
from product_management import product_management
from procurement import procurement_app

# app = Flask(__name__)
if getattr(sys, 'frozen', False):
  template_folder = os.path.join(sys._MEIPASS, 'templates')
  static_folder = os.path.join(sys._MEIPASS, 'static')
  app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
  app = Flask(__name__)

# 静态文件缓存时间设置
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config.from_object(config)
app.config['SECRET_KEY'] = os.urandom(24)  # 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。


# cc管理员
@app.route('/admin')
def index_adm():
    personName = session['username']
    return render_template('adm_index.html',personName=personName)

# cc 操作员
@app.route('/oprator')
def index_operator():
    personName = session['username']
    Authority = session['authority']
    return render_template('operator_index.html',Authority=Authority,personName=personName)

# cc 登陆
@app.route('/', methods=['GET', 'POST'])
def user_login():
    print(session)
    # if session:
    if session.get('username'):
        username = session['username']
        # session.pop('username')
        print('session 不为空 ', username)
        print("开始调用函数获取用户类型")
        Authority = login_Authority(username)
        if Authority == '888':
            print("admin login!")
            return redirect(url_for('index_adm'))
        else:
            print("oprator login!")
            return redirect(url_for('index_operator'))

    # print(session[0])
    if request.method == "POST":
        session.clear()
        print(request.form)
        user = User()
        stu_id = user.id = request.form["user_id"]
        user.pwd = request.form["user_pwd"]
        Authority = login_Authority(user.id)
        print("测试Authorith 输出数字", Authority)
        # print("admin login", Authority)
        session['authority'] = Authority
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
            session.clear()
            return render_template('user_login.html', message=message)
        print("name:  pwd:", user.name, user.pwd)
        return redirect(url_for("user_login"))  # 跳到主页
    return render_template('user_login.html')


# cc退出系统
@app.route('/out', methods=['GET', 'POST'])
def out():
    session.clear()
    return redirect(url_for('user_login'))

# cc 管理员 人员管理
@app.route('/person_management',methods=['GET', 'POST'])
def person_management():
    return render_template('person_management.html')

# cc 人员管理_查看人员
@app.route('/show_person',methods=['GET', 'POST'])
def show_person():
    personName = session['username']
    temp = list(show_allperson())
    person = []
    for i in temp:
        i = list(i)
        if i[3] == '888':
            i[3] = "管理员"
        else:
            a = i[3][0]
            b = i[3][1]
            c = i[3][2]
            sa = "物料" + person_authority(a)
            sb = "成品" + person_authority(b)
            sc = "采购" + person_authority(c)
            i[3] = sa + "、" + sb + "、" + sc
        person.append(i)
    # print(person)
    return render_template('person_management_show.html', person=person, personName=personName)

# cc 查看人员管理的数字映射权限
def person_authority(auth):
    return {
        '0': "无权限",
        '1': "读权限无金额",
        '2': "读权限有金额",
        '3': "修改权限",
    }.get(auth,'error')

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
        # print(user.name, user.pwd, user.authority)
        cc_add_account(user.name, user.pwd, int(user.authority))
        add_message = "添加成功"
        return render_template('add_person.html', add_message=add_message, form=form)
    return render_template('add_person.html',form=form)

# cc 人员管理_删除人员
@app.route('/delete_person',methods=['GET', 'POST'])
def delete_person():
    result = cc_findname()
    temp = list(show_allperson())
    person = []
    for i in temp:
        i = list(i)
        if i[3] == '888':
            i[3] = "管理员"
        else:
            a = i[3][0]
            b = i[3][1]
            c = i[3][2]
            sa = "物料" + person_authority(a)
            sb = "成品" + person_authority(b)
            sc = "采购" + person_authority(c)
            i[3] = sa + "、" + sb + "、" + sc
        person.append(i)
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
    temp = list(show_allperson())
    person = []
    for i in temp:
        i = list(i)
        if i[3] == '888':
            i[3] = "管理员"
        else:
            a = i[3][0]
            b = i[3][1]
            c = i[3][2]
            sa = "物料" + person_authority(a)
            sb = "成品" + person_authority(b)
            sc = "采购" + person_authority(c)
            i[3] = sa + "、" + sb + "、" + sc
        person.append(i)
    form = ChangeForm()
    if request.method == "POST":
        print("修改人员权限")
        id = form.data['personName']
        authority = form.data['status'] + "" + form.data['statusPro'] + "" + form.data['statusPur']
        cc_changeAuthority(id,authority)
        change_message = "修改成功"
        return render_template('change_person.html', change_message=change_message, form=form, person=person)
    return render_template('change_person.html', form=form, person=person)

# cc 修改密码
@app.route('/cc_change_pass', methods=['GET', 'POST'])
def cc_change_pass():
    print("修改界面", session['username'])
    # sql 修改数据库中的密码
    # fun_changepassword(user)
    if request.method == "POST":
        user = NewUser()
        user.name = session['username']
        print("需要修改的用户是", user.name)
        user.pwd = select_pass(user.name)
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
            update_pass(user.name, user.pwd)
            print("密码修改成功")
            print("密码修改成功，请推出当前界面重新登陆")
            # return 'ok'
            message = "密码修改成功，请重新登陆"
            # session.pop(user.name)
            session.clear()
            return redirect(url_for("user_login"))  # 跳到主页
            # return render_template('user_login.html', message=message)
        else:
            message = "旧密码有误，请重新输入"
            print("旧密码有误，请重新输入")
            return render_template('changepassword.html', message=message)
            #   session.pop(user.name)
    else:
        return render_template('changepassword.html')

# lh 查看物料信息
@app.route('/show_material', methods=['GET', 'POST'])
def show_material():
    materialCode = ''
    materialName = ''
    materialType = ''
    materialFactory = ''
    personName = session['username']
    Authority = session['authority']
    Authority = Authority[0]
    if request.method == "POST":
        materialCode = request.form["materialCode"]
        materialName = request.form["materialName"]
        materialType = request.form["materialType"]
        materialFactory = request.form["materialFactory"]
    materialAll = dao_show_material(materialCode, materialName, materialType, materialFactory)
    materialinfoAll = dao_show_materialinfo()
    materialoutinAll = dao_show_materialoutin()
    # print(materialAll)
    return render_template('material_index.html', materialAll=materialAll, materialCode=materialCode,
                           materialName=materialName, materialType=materialType,
                           materialFactory=materialFactory,Authority=Authority,personName=personName)

# lh 物料出入库
@app.route('/material_outorin/<mCode>', methods=['GET', 'POST'])
def material_outorin(mCode):
    material_init = dao_show_materialoutorin(mCode)
    materialinfoAll = dao_show_materialinfo()
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
           if dao_material_out(materialCode, materialName, materialType, m_price,materialFactory,mNum,mDepartment,mDcNum,materialTime,personName):
                print("出库成功")
                message = "出库成功"
                return render_template('material_outorin.html', message=message, materialinfoAll=materialinfoAll)
           else:
                message = "出库失败,请重新填写"
                print("出库失败,请重新填写")
                return render_template('material_outorin.html', message=message, materialinfoAll=materialinfoAll)
                #   session.pop(user.name)
        elif isinorout == '0':
            # print("入库！")

            if dao_material_in(materialCode, materialName, materialType, m_price,materialFactory,mNum,mDepartment,mDcNum,materialTime,personName):
                print("入库成功")
                message = "入库成功"
                return render_template('material_outorin.html', message=message, materialinfoAll=materialinfoAll)
            else:
                message = "入库失败,请重新填写"
                print("入库失败,请重新填写")
                return render_template('material_outorin.html', message=message, materialinfoAll=materialinfoAll)
                #   session.pop(user.name)
        else :
            materialCode = request.form["materialCode"]
            materialName = request.form["materialName"]
            materialType = request.form["materialType"]
            materialFactory = request.form["materialFactory"]

            mDepartment = request.form['mDepartment']
            m_price = request.form['m_price']
            if dao_material_edit(materialCode, materialName, materialType, mDepartment,m_price, materialFactory,mCode):
                print("修改成功")
                message = "修改成功"
                return render_template('material_outorin.html', message=message, materialinfoAll=materialinfoAll)
            else:
                message = "修改成功,请重新填写"
                return render_template('material_outorin.html', message=message, materialinfoAll=materialinfoAll)

    else:
        # print(material_init)
        for i in material_init:
            materialCode = i[0]
            materialName = i[1]
            materialType = i[2]
            mDepartment = i[3]
            m_price = i[4]
            materialFactory = i[7]

        return render_template('material_outorin.html',materialCode=materialCode,materialName=materialName,
                               materialType=materialType,mDepartment=mDepartment,m_price=m_price,
                               materialFactory=materialFactory,personName=personName,materialinfoAll=materialinfoAll)

# xijiawei
# 添加“product_management.py”蓝本
app.register_blueprint(product_management)

app.register_blueprint(procurement_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    #pass