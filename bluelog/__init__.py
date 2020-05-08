# -*- coding: utf-8 -*-



from flask import Flask, render_template, request
from bluelog.settings import config
from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.gly import gly_bp
from bluelog.blueprints.user import user_bp
from bluelog.extensions import db
from bluelog.models import Admin,Post
from flask_login import LoginManager
from flask_dropzone import Dropzone
from flask_ckeditor import CKEditor, CKEditorField
from flask_wtf.csrf  import CSRFProtect,generate_csrf
import flask_whooshalchemyplus
from jieba.analyse.analyzer import ChineseAnalyzer




import os


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


#实例化类
dropzone = Dropzone()
login_manager = LoginManager() #实例化登录类
ckeditor = CKEditor()
csrf = CSRFProtect()
def create_app(config_name=None):
    #选择配置名
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')   

    app = Flask('bluelog')
    app.config.from_object(config[config_name])    



    app.config['CKEDITOR_SERVE_LOCAL'] = True
    app.config['CKEDITOR_HEIGHT'] = 300
    app.config['CKEDITOR_FILE_UPLOADER'] = 'admin.upload'
    # app.config['CKEDITOR_ENABLE_CSRF'] = True  # if you want to enable CSRF protect, uncomment this line
    app.config['UPLOADED_PATH'] = os.path.join(basedir, 'uploads')
    app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True   #开启代码语法高亮


    #注册蓝本
    app.register_blueprint(admin_bp)   
    app.register_blueprint(gly_bp) 
    app.register_blueprint(user_bp) 
    
    
    #初始化扩展
    db.init_app(app)  
    csrf.init_app(app)     
    login_manager.init_app(app)   #初始化登录类
    dropzone.init_app(app)
    ckeditor.init_app(app)
    flask_whooshalchemyplus.init_app(app)
    
    register_shell_context(app)


    

    return app


#全局上下文变量
def register_shell_context(app):
    @app.context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin,pp='春江花月夜',Post=Post)


#关于登录必须的一个回调函数
@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import Admin
    user=Admin.query.get(int(user_id))
    return user

