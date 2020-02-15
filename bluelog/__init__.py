# -*- coding: utf-8 -*-



from flask import Flask, render_template, request
from bluelog.settings import config
from bluelog.blueprints.admin import admin_bp
from bluelog.extensions import db
from bluelog.models import Admin
import os
##
##

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    #选择配置名
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')   

    app = Flask('bluelog')
    app.config.from_object(config[config_name])    

    #注册蓝本
    app.register_blueprint(admin_bp)    
    
    
    #初始化扩展
    db.init_app(app)                    

    
    
    register_shell_context(app)

    return app


def register_shell_context(app):
    @app.context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin)