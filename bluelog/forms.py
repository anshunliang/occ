# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, TextAreaField,SelectField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField



#文章表单
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    body = CKEditorField('Body', validators=[DataRequired()])   #此扩展必须联网或者加载之前的缓存才会好看
    submit = SubmitField()
