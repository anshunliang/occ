import os,sys,re,json 
from flask import Flask,render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import LoginManager,login_user,login_required, logout_user,current_user
from bluelog.models import Admin
from bluelog.extensions import db
from bluelog.models import Admin,Category,Post
from bluelog.forms import CategoryForm,UploadForm   ###导入同级目录中的表单定义文件
from flask_dropzone import random_filename

import flask_whooshalchemyplus

user_bp=admin_bp = Blueprint('user', __name__)  #定义蓝本


#专门文件上传函数
@user_bp.route('/up',methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename =random_filename(f.filename)
        f.save(os.path.join('F:\\LCC\\tupian',filename))  # 保存文件
        
    rootdir = "F:\\LCC\\tupian"
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件   
    print(list)
    return render_template('up.html',form = form,list=list)







#API返回JSON数据
@user_bp.route('/user')
def use1():
    
    post=Post.query.get_or_404(1)
    x='plplpl'
    a=json.dumps(post.body)
    return a