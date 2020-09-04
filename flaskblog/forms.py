from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, TextAreaField, SelectField, \
    DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

from flaskblog.models import User, Category, Article


class LoginForm(FlaskForm):
    username = StringField('帐号', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField(label='记住我', default=False)
    submit = SubmitField('登 录')

class RegistForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 16, message='用户名长度要在1和16之间')])
    email = StringField('邮箱', validators=[DataRequired(), Length(6, 64, message='邮件长度要在6和64之间'),
                        Email(message='邮件格式不正确！')])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='密码必须一致！')])
    password2 = PasswordField('重输密码', validators=[DataRequired()])
    submit = SubmitField('注 册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被注册！')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册！')


class ArticleForm(FlaskForm):
    id = HiddenField('id')
    title = StringField('标题', validators=[DataRequired('请录入标题')])
    name = StringField('标识名称', render_kw={'placeholder': '自定义路径'})
    content = TextAreaField('文章内容')
    category_id = SelectField('分类', coerce=int, default=1, validators=[DataRequired('请选择分类')])
    tags = StringField('标签')
    state = HiddenField('状态', default=0)
    thumbnail = HiddenField('缩略图', default='/static/img/thumbnail.jpg')
    summary = TextAreaField('概述', validators=[Length(0, 300, message='长度必须设置在300个字符内')])
    timestamp = DateTimeField('发布时间', default=datetime.now)
    save = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(category.id, category.title)
                                    for category in Category.query.order_by(Category.title).all()]

    def validate_name(self, field):
        """
        验证文章名称标识的唯一性
        """
        name = field.data
        articles = Article.query.filter_by(name=name).all()
        if len(articles) > 1:
            raise ValidationError('路径已经存在')
        if len(articles) == 1 and self.id.data and articles[0].id != int(self.id.data):
            raise ValidationError('路径已经存在')
