from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import current_user, login_user, logout_user

from flaskblog import db
from flaskblog.forms import LoginForm, RegistForm
from flaskblog.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login',methods = ["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm(prefix='login')
    print("正在尝试登录.....")
    if form.validate_on_submit():
        print("表单正在校验....")
        user = User.query.filter_by(username = form.username.data.strip()).first()
        if user is None:
            print("该账号未注册!")
            flash({'error':'该账号未注册!'})
        elif user is not None and user.verify_password(form.password.data.strip()) and user.status:
            login_user(user=user,remember=form.remember_me.data)
            print("欢迎{}登录成功!".format(user.username))
            flash({"success":'欢迎{}登录成功!'.format(user.username)})
            print(url_for('blog.index'))
            return redirect(url_for('blog.index'))
        elif not user.status:
            print("用户已被管理员注销")
            flash({'error': '用户已被管理员注销！'})
        elif not user.verify_password(form.password.data.strip()):
            print("密码不正确！")
            flash({'error': '密码不正确！'})

    return render_template('login.html',form =form )


@auth_bp.route('/regist',methods = ["GET","POST"])
def regist():
    form = RegistForm(prefix='regist')

    if form.validate_on_submit():

        user_username = User.query.filter_by(username = form.username.data.strip()).first()
        user_email = User.query.filter_by(email = form.email.data.strip()).first()
        if user_username is not None:
            flash({"error":"用户名已存在!"})
        elif user_email is not None:
            flash({"error": "邮箱已被注册，请更换邮箱注册!"})
        else:
            if form.password.data.strip() != form.password2.data.strip() :
                flash({"error":"两次密码不一致,请重新重复密码."})
            else:
                user = User(username= form.username.data.strip(),email=form.email.data.strip(),
                             status=True,role=False)
                user.password = form.password.data.strip()
                db.session.add(user)
                db.session.commit()
                login_user(user = user)
                flash({'success': '欢迎{}注册成功'.format(user.username)})
                # TODO: 多用户登录.待做......
                return redirect(request.args.get('next',url_for('auth.login')))
    return render_template('registe.html', form=form)

@auth_bp.route('/logout')
def logout():

    logout_user()
    print("当前用户已退出登录状态.")
    flash({"success":"当前用户已退出登录状态."})
    return redirect(url_for('blog.index'))


