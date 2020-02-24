# -*- coding: utf-8 -*-



from flask import Flask, render_template, request
from bluelog.settings import config
from bluelog.blueprints.admin import admin_bp
from bluelog.extensions import db
from bluelog.models import Admin
from flask_login import LoginManager
from flask_dropzone import Dropzone
from flask_ckeditor import CKEditor, CKEditorField
from flask_wtf.csrf  import CSRFProtect,generate_csrf


import os
##
##

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
dropzone = Dropzone()
login_manager = LoginManager() 
ckeditor = CKEditor()
csrf = CSRFProtect()
def create_app(config_name=None):
    #选择配置名
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')   

    app = Flask('bluelog')
    app.config.from_object(config[config_name])    



    app.config['CKEDITOR_SERVE_LOCAL'] = True
    app.config['CKEDITOR_HEIGHT'] = 400
    app.config['CKEDITOR_FILE_UPLOADER'] = 'admin.upload'
    # app.config['CKEDITOR_ENABLE_CSRF'] = True  # if you want to enable CSRF protect, uncomment this line
    app.config['UPLOADED_PATH'] = os.path.join(basedir, 'uploads')
    
    #注册蓝本
    app.register_blueprint(admin_bp)    
    
    
    #初始化扩展
    db.init_app(app)  
    csrf.init_app(app)     
    login_manager.init_app(app)
    dropzone.init_app(app)
    ckeditor.init_app(app)
    
    register_shell_context(app)


    

    return app


def register_shell_context(app):
    @app.context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin)

@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import Admin
    user=Admin.query.get(int(user_id))
    return user

