# -*- coding: utf-8 -*-

import os

from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory

from bluelog.models import Admin
from bluelog.extensions import db

admin_bp = Blueprint('admin', __name__)  #定义蓝本


@admin_bp.route('/', methods=['GET', 'POST'])
def s():
    
    if request.method=='POST':
        a=request.form['username']
        b=request.form['password']

        message = Admin(username=a, password_hash=b)
        db.session.add(message)
        db.session.commit()

        return render_template('x.html')
    return render_template('x.html')
   