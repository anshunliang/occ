# -*- coding: utf-8 -*-

from datetime import datetime


from bluelog.extensions import db
from flask_login import UserMixin

#用户模型
class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

#类别模型
class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),unique=True)
    posts = db.relationship('Post', back_populates='category')    #与文章的集合关系属性



#文章模型
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(60))
    body=db.Column(db.Text)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow,index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))      #定义到分类模型的外键，注意在多的这一侧建立外键 
    category = db.relationship('Category', back_populates='posts')          #与分类模型的标量关系属性


