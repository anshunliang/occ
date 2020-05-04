# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from wtforms.fields import SelectField, SubmitField
from flask_ckeditor import CKEditorField
from bluelog.models import Admin,Category,Post



#登录表单
class LoginForm(Form):
    
    
    name = StringField('name', validators=[DataRequired()])

    password = StringField('password', validators=[DataRequired()])

    

#文章表单
class PostForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    body = CKEditorField('Body', validators=[DataRequired()])   #此扩展必须联网或者加载之前的缓存才会好看
    category = SelectField('Category', coerce=int, default=1)
    submit = SubmitField()
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]   


class CategoryForm(Form):
    name=StringField('title',validators=[DataRequired()])

