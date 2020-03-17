from datetime import timedelta

from flask import Flask, url_for, render_template, request, redirect, session, jsonify

from form import *
from db import *
import config
import os
import sys

from product import product_app
from procurement import procurement_app
from material import material_app

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
    # if session:
    if session.get('username'):
        username = session['username']
        # session.pop('username
        authority = select_user_authority(username)
        if authority == '888':
            print("admin login!")
            return redirect(url_for('index_adm'))
        else:
            print("oprator login!")
            return redirect(url_for('index_operator'))

    # print(session[0])
    if request.method == "POST":
        session.clear()
        username = request.form["username"]
        password = request.form["password"]
        print("name:  pwd:", username, password)
        if login_check(username,password):
            session['username'] = username
            authority = select_user_authority(username)
            session['authority'] = authority
            if authority == '888':
                print("admin login!")
                return redirect(url_for('index_adm'))
            else:
                print("oprator login!")
                return redirect(url_for('index_operator'))
        else:
            message = "用户名或者密码错误"
            session.clear()
            return render_template('user_login.html', message=message) # 跳到主页
    elif request.method == "GET":
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

# cc 查看人员管理的数字映射权限
def person_authority(auth):
    return {
        '0': "无权限",
        '1': "读权限无金额",
        '2': "读权限有金额",
        '3': "修改权限",
        '4': "部分修改权限",
    }.get(auth,'error')

# xijiawei
def show_all_users():
    result = select_all_users()
    users = []
    for i in result:
        user = [i[0], i[1], i[2]]
        users.append(user)
        if i[3] == '888':
            user.append("管理员")
        else:
            user.append("物料" + person_authority(i[3][0]) + "、" + "成品" + person_authority(
                i[3][1]) + "、" + "采购" + person_authority(i[3][2]))
    return users

# cc 人员管理_查看人员
@app.route('/show_users',methods=['GET', 'POST'])
def show_users():
    username = session['username']
    users = show_all_users()
    return render_template('person_management_show.html', users=users, username=username)

# cc 人员管理_增加人员
@app.route('/add_user',methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if request.method == "POST":
        # username=request.form["username"]
        # authority = form.data['materialAuth'] + form.data['productAuth'] + form.data['procurementAuth']
        data = request.get_json()
        username = data["username"]
        authority = data['materialAuth'] + data['productAuth'] + data['procurementAuth']
        if select_user(username):
            return jsonify({'ok': False})
        else:
            insert_user(username, '88888888', authority)
            return jsonify({'ok': True})
    elif request.method == "GET":
        return render_template('add_person.html',form=form)

# cc 人员管理_删除人员
@app.route('/delete_user',methods=['GET', 'POST'])
def delete_user():
    form = UserForm()
    if request.method == "POST":
        userid = form.data['userid']
        delete_userByID(userid)
        delete_message = "删除成功"
        users = show_all_users()
        choices = select_all_users_for_selector()
        form.userid.choices = choices
        return render_template('delete_person.html', delete_message=delete_message, form=form, users=users)
    elif request.method == "GET":
        users = show_all_users()
        choices = select_all_users_for_selector()
        form.userid.choices = choices
        return render_template('delete_person.html', form=form, users=users)

# cc 人员管理_权限管理
@app.route('/change_authority',methods=['GET', 'POST'])
def change_authority():
    form = UserForm()
    if request.method == "POST":
        userid = form.data['userid']
        authority = form.data['materialAuth'] + form.data['productAuth'] + form.data['procurementAuth']
        update_user_authority(userid, authority)
        change_message = "修改成功"
        users = show_all_users()
        choices = select_all_users_for_selector()
        form.userid.choices = choices
        return render_template('change_person.html', change_message=change_message, form=form, users=users)
    elif request.method == "GET":
        users = show_all_users()
        choices = select_all_users_for_selector()
        form.userid.choices = choices
        return render_template('change_person.html', form=form, users=users)

# cc 修改密码
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    print("修改界面", session['username'])
    # sql 修改数据库中的密码
    # fun_changepassword(user)
    if request.method == "POST":
        username = session['username']
        password = select_user_password(username)
        oldpassword = request.form["oldpassword"]
        newpassword = request.form["newpassword"]
        renewpassword = request.form["renewpassword"]
        if oldpassword!=password:
            message = "旧密码有误，请重新输入"
            print("旧密码有误，请重新输入")
            return render_template('changepassword.html', message=message)
        else:
            if newpassword != renewpassword:
                message = "两次密码不一致，请重新输入"
                print("两次密码不一致，请重新输入")
                return render_template('changepassword.html', message=message)
            else:
                update_user_password(username, newpassword)
                message = "密码修改成功，请重新登陆"
                # session.pop(user.name)
                session.clear()
                return redirect(url_for("user_login"))  # 跳到主页
    else:
        return render_template('changepassword.html')

# xijiawei
# 添加“material.py”蓝本
app.register_blueprint(material_app)
# xijiawei
# 添加“product.py”蓝本
app.register_blueprint(product_app)
# xijiawei
# 添加“procurement.py”蓝本
app.register_blueprint(procurement_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    #pass