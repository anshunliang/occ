import os,sys,re,json 
from flask import Flask,render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import LoginManager,login_user,login_required, logout_user,current_user
from bluelog.models import Admin
from bluelog.extensions import db
from bluelog.models import Admin,Category,Post
from bluelog.forms import CategoryForm,UploadForm   ###导入同级目录中的表单定义文件
from flask_dropzone import random_filename

import flask_whooshalchemyplus,platform

user_bp=admin_bp = Blueprint('user', __name__)  #定义蓝本


#专门文件上传函数
@user_bp.route('/up',methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if(platform.system()=='Windows'):
        rootdir = "F:\\LCC\\tupian"                           #开发环境中使用
    else:
        rootdir ="/root/l/occ/bluelog/static/tupian"          #云服务器上使用
    if form.validate_on_submit():
        f = form.photo.data
        filename=f.filename
        f.save(os.path.join(rootdir,filename))  # 保存文件

    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件   
    print(list)
    return render_template('up.html',form = form,list=list)




#下载文件

@user_bp.route("/download", methods=['GET'])
def download_file():
    filename=request.args.get("filename") 
    
    if(platform.system()=='Windows'):
        rootdir = "F:\\LCC\\tupian"
    else:
        rootdir ="/root/l/occ/bluelog/static/tupian"

    return send_from_directory(rootdir, filename, as_attachment=True)




#删除服务器上的文件
@user_bp.route('/delete',methods=['GET','POST'])
def delete():
    filename=request.args.get("filename") 
    
    if(platform.system()=='Windows'):
        os.remove("F:\\LCC\\tupian"+"\\"+filename)                     #开发环境中使用
    else:
        os.remove("/root/l/occ/bluelog/static/tupian"+"/"+filename)    #云服务器上使用
    
    return redirect(url_for('user.upload'))



@user_bp.route("/<filename>")
def player(filename):
    if(platform.system()=='Windows'):
        path = "..//static//tupian"+"//"+filename           #开发环境中使用
    else:
        path = "../static/tupian"+"/"+filename              #云服务器上使用
    return render_template('player.html',path=path)



#API返回JSON数据
@user_bp.route('/user')
def use1():
    
    post=Post.query.get_or_404(1)
    x='plplpl'
    a=json.dumps(post.body)
    return a