# -*- coding: utf-8 -*-

import os
import re
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import LoginManager,login_user,login_required, logout_user,current_user
from bluelog.models import Admin
from bluelog.extensions import db
from bluelog.models import Admin,Category,Post
from bluelog.forms import PostForm,LoginForm   ###导入同级目录中的表单定义文件
from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success
from flask import send_from_directory
from flask_dropzone import random_filename
import flask_whooshalchemyplus






admin_bp = Blueprint('admin', __name__)  #定义蓝本
ckeditor = CKEditor()


global tp   #定义文件名的全局变量
tp=list()   #初始化为一个列表
#主页函数

@admin_bp.route('/',defaults={'page':1},methods=['post','get'])
@admin_bp.route('/page/<int:page>', methods=['GET', 'POST'])
def a(page):
    
    lg=LoginForm() 
    per_page=3
    pagination= Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=per_page)
    m=pagination.items
    if request.method=='POST':
        a=request.form['username']
        b=request.form['password']

        message = Admin(username=a, password_hash=b)
        db.session.add(message)
        db.session.commit()


        return render_template('a.html')
    return render_template('a.html',m=m,page=page,pagination=pagination,lg=lg)


#python分类展示函数
@admin_bp.route('/d')
def d():
    lg=LoginForm()   
    page=request.args.get('page',1,type=int)
    per_page=3
    pagination=Post.query.filter_by(category_id=Category.query.filter_by(name='python').first().id).order_by(Post.timestamp.desc()).paginate(page,per_page=per_page)
    m=pagination.items
    return render_template('a.html',m=m,page=page,pagination=pagination,lg=lg)

#labview分类展示函数
@admin_bp.route('/e')
def e():
    lg=LoginForm()
    page=request.args.get('page',1,type=int)
    per_page=3
    pagination=Post.query.filter_by(category_id=Category.query.filter_by(name='labview').first().id).order_by(Post.timestamp.desc()).paginate(page,per_page=per_page)
    m=pagination.items
    return render_template('a.html',m=m,page=page,pagination=pagination,lg=lg)

#西门子工业控制分类展示函数
@admin_bp.route('/f')
def f():
    lg=LoginForm()
    page=request.args.get('page',1,type=int)
    per_page=3
    pagination=Post.query.filter_by(category_id=Category.query.filter_by(name='西门子工业控制').first().id).order_by(Post.timestamp.desc()).paginate(page,per_page=per_page)
    m=pagination.items
    return render_template('a.html',m=m,page=page,pagination=pagination,lg=lg)

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
    form=LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        username=request.form['name']
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
    #接收文章
    if wz.validate_on_submit():
        title = wz.title.data
        body = wz.body.data   #从这个body里面提取出图片名
        bf=body[20:33]
        category = Category.query.get(request.form['category'])
        #使用正则表达式匹配文件名
        #x=re.findall(r'\bf\S*?G\b',body) #此处匹配f开头，G结束的字符串

        tpn=""   #初始化图片名字符串
        for i in tp:
            tpn=tpn+i+","
        tp.clear()  #清空全局列表  
      
        n=Post(title=title,body=body,category=category,tpname=tpn)
        db.session.add(n)
        db.session.commit()
        return redirect(url_for('admin.a'))
    '''
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
        
        # return redirect(url_for('admin.upload'))  #提交文章后，重定向到前台
        #return render_template('tj.html',wz=wz)
    '''
    return render_template('tj.html',wz=wz)

#删除文章
@admin_bp.route('/delete/<int:post_id>',methods=['GET','POST'])
def delete(post_id):
    n=Post.query.get_or_404(post_id)
    x=n.tpname.split(",")   #待删除的图片名列表
    for i in x:
        if i=="":
            break
        os.remove("F:\\LCC\\bluelog\\templates\\files"+"\\"+i)
  
    db.session.delete(n)
    db.session.commit()
    return redirect(url_for('admin.a'))


#接收图片

@admin_bp.route('/x', methods=['GET', 'POST'])
def x():
    print('kkkkkkkkkkkkkkkkkkkkkkk')
    if request.method == 'POST':  # 如果请求类型为POST，说明是文件上传请求
        f = request.files.get('file')  # 获取文件对象
        print(f.filename)
        f.save(os.path.join('F:\\LCC\\tupian', f.filename))  # 保存文件
        return render_template('a.html')
    
    return render_template('a.html')


#测试页面
@admin_bp.route('/xx', methods=['GET', 'POST'])
def xx():
    
    if request.method == 'POST':
        data = request.form.get('ckeditor')
        print(data)
    
    return render_template('test.html')



#文章视图
@admin_bp.route('/post/<int:post_id>',methods=['POST','get'])
def show_post(post_id):
    post=Post.query.get_or_404(post_id)
    
    return render_template('show.html',post=post)


@admin_bp.route('/files/<filename>')
def uploaded_files(filename):
    path = 'F:\\LCC\\bluelog\\templates\\files'  #这个地址要和  def upload()  里面保存的地址一样
    return send_from_directory(path, filename)


@admin_bp.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[1].lower()
   
    filename=random_filename(f.filename)
    tp.append(filename)
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join('F:\\LCC\\bluelog\\templates\\files', filename))
    url=url_for('admin.uploaded_files', filename=filename)

    return upload_success(url=url)


#获取搜索框内容，然后重定向到搜索函数
@admin_bp.route('/search', methods = ['POST'])
def search():
    if request.method=='POST':
        flask_whooshalchemyplus.index_one_model(Post)
        if not request.form['search']:
            return redirect(url_for('.index'))
        return redirect(url_for('.search_results', query = request.form['search']))
 
#搜索，返回结果
@admin_bp.route('/search_results/<query>')
def search_results(query):
    results = Post.query.whoosh_search(query).all()
    print(query)
    print(results)
    return render_template('search_results.html', query = query, results = results)
