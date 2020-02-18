# -*- coding: utf-8 -*-

import os

from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import LoginManager,login_user,login_required, logout_user,current_user
from bluelog.models import Admin
from bluelog.extensions import db
from bluelog.models import Admin



admin_bp = Blueprint('admin', __name__)  #定义蓝本

#主页函数
@admin_bp.route('/', methods=['GET', 'POST'])
def a():
    
    if request.method=='POST':
        a=request.form['username']
        b=request.form['password']

        message = Admin(username=a, password_hash=b)
        db.session.add(message)
        db.session.commit()


        return render_template('a.html')
    return render_template('a.html')

#注册函数  
@admin_bp.route('/zhuce', methods=['GET', 'POST'])
def zhuce():
    
    if request.method=='POST':
        username = request.form['username']
        password_hash=request.form['password_hash']
        if Admin.query.filter_by(username=username).first():#如果用户名已经存在
                return redirect(url_for('admin.a',b='用户名已存在'))
        message = Admin(username=username, password_hash=password_hash)
        db.session.add(message)
        print("注册成功")
        db.session.commit()
        return redirect(url_for('admin.a')) #防止刷新页面时重复提交表单,并且注册后重定向到主页


#登录函数
@admin_bp.route('/login',methods=['get','post'])
def login():
        if request.method=='POST':
                username=request.form['username']
                password=request.form['password']
                if not Admin.query.filter_by(username=username).first():
                        return redirect(url_for('admin.a',b='用户名不存在'))
                m=Admin.query.filter_by(username=username).first()
                n=m.password_hash
                if password==n:
                    print("登录成功")
                    login_user(m,remember = True)
                    return redirect(url_for('admin.a'))
        return redirect(url_for('admin.a',s='密码错误'))

#登出函数
#@login_manager.user_loader
@admin_bp.route('/logout')
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    print('退出登录')
    return redirect(url_for('admin.a'))  # 重定向回首页