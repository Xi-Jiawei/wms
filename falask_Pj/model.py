# coding: utf-8
class User:
    def __init__(self, id = None,name=None, pwd=None, ruletype=None, gender=None,
                 email=None, tel=None, introduce=None):
        self.id = id
        self.name = name
        self.pwd = pwd
        self.ruletype = ruletype  #区分人员类型
        self.gender = gender
        self.email = email
        self.tel = tel
        self.introduce = introduce

class Student:
    def __init__(self, studentid = None,name=None, pwd=None, gender=None,
                 email=None, tel=None, introduce=None):
        self.studentid = studentid
        self.name = name
        self.pwd = pwd
        self.gender = gender
        self.email = email
        self.tel = tel
        self.introduce = introduce

class NewUser:
    def __init__(self, name=None, pwd=None, authority=None):
        self.name = name
        self.pwd = 88888888
        self.authority = authority
