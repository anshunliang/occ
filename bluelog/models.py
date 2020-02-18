# -*- coding: utf-8 -*-

from datetime import datetime


from bluelog.extensions import db
from flask_login import UserMixin

class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
