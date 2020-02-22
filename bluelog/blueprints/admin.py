# -*- coding: utf-8 -*-

import os

from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import LoginManager,login_user,login_required, logout_user,current_user
from bluelog.models import Admin
from bluelog.extensions import db
from bluelog.models import Admin,Category,Post
from bluelog.forms import PostForm   ###导入同级目录中的表单定义文件


admin_bp = Blueprint('admin', __name__)  #定义蓝本

#主页函数
#@admin_bp.route('/',defaults={'page':1},methods=['post','get'])
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



#创建分类
@admin_bp.route('/cjfl', methods=['GET', 'POST'])
def cjfl():
    if request.method=='POST':
        name=request.form['name']
        message = Category(name=name)
        db.session.add(message)
        print("创建分类成功")
        db.session.commit()
        return redirect(url_for('admin.a'))
    return redirect(url_for('admin.a'))




#添加文章
@admin_bp.route('/tj', methods=['GET', 'POST'])
def tj():
    wz=PostForm()
    if request.method == 'POST':  # 如果请求类型为POST，说明是文件上传请求
        title = request.form['title']
        category = Category.query.get(request.form['category'])
        body = request.form['body']
        print(body)
        n=Post(title=title,body=body,category=category)
        db.session.add(n)
        db.session.commit()
        print('交文章成功')
        return render_template('a.html')
    return render_template('tj.html',wz=wz)


#接收图片
@admin_bp.route('/x', methods=['GET', 'POST'])
def x():
    if request.method == 'POST':  # 如果请求类型为POST，说明是文件上传请求
        f = request.files.get('file')  # 获取文件对象
        print(f.filename)
        f.save(os.path.join('F:\\LCC\\tupian', f.filename))  # 保存文件
        return render_template('a.html')
    
    return render_template('a.html')

#测试页面
@admin_bp.route('/xx', methods=['GET', 'POST'])
def xx():
    
    
    return render_template('test.html')



