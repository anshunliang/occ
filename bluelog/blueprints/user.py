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


user_bp=admin_bp = Blueprint('user', __name__)  #定义蓝本

@user_bp.route('/user')
def user():
    
    
    return "个人主页"