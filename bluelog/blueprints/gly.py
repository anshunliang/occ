import os
import re
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import LoginManager,login_user,login_required, logout_user,current_user
from bluelog.models import Admin
from bluelog.extensions import db
from bluelog.models import Admin,Category,Post
from bluelog.forms import CategoryForm   ###导入同级目录中的表单定义文件
from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success
from flask import send_from_directory
from flask_dropzone import random_filename
import flask_whooshalchemyplus


gly_bp=admin_bp = Blueprint('gly', __name__)  #定义蓝本

@gly_bp.route('/gly')
def gly():
    cf=CategoryForm()  #
    category=Category.query.all()   #获取所有类名
    
    return render_template('gly.html',category=category,cf=cf)


#删除该分类
@gly_bp.route('/shanchu')
def shanchu():
    id=request.args.get('category_id')  #获取待删除的类别id
    print("获取待删除的类别id"+id)
    post=Post.query.filter_by(category_id=id).all() #获取该类别下的所有文章
    
    #删除该分类下的所有文章
    for i in post:
        n=Post.query.get_or_404(i.id)
        x=n.tpname.split(",")
        for j in x:
            if j=="":
                #break
                pass
            if j!="":
                os.remove("F:\\LCC\\bluelog\\templates\\files"+"\\"+j)
        db.session.delete(n)
        db.session.commit()
    
    #删除分类
    
    x=Category.query.get_or_404(id)
    db.session.delete(x)
    db.session.commit()

    return redirect(url_for('.gly'))

#增加分离
@gly_bp.route('/add',methods=['get','post'])
def add():
    form=CategoryForm()
    if request.method=='POST' and form.validate_on_submit():
        name=request.form['name']
        n=Category(name=name)
        db.session.add(n)
        db.session.commit()
    return redirect(url_for('gly.gly'))
