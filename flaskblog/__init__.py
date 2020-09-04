import os

import click
from flask import Flask


# 绝对路径
from flaskblog.extensions import db, bootstrap
from flaskblog.models import Category, Tag, Article
from flaskblog.settings import config


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    # 创建app并初始化app,返回app
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG",'development')

    app = Flask(__name__)
    app.config["CONFIG_NAME"] = config_name
    app.config.from_object(config[config_name])

    """使用工厂函数,初始化程序实例."""
    #
    bootstrap.init_app(app)

    # 注册蓝图
    register_blueprints(app)
    # 初始化app
    register_extensions(app)
    # 注册一些命令行命令,便于操作数据库
    register_commands(app)
    # 注册上下文管理器, 返回一些全局变量，所有页面都可使用
    register_template_context(app)


    return app


def register_blueprints(app):
    """
    注册蓝图:将多个路由使用蓝图注册。
    :param app:
    :return:
    """
    # 注册 blog 蓝图
    from flaskblog.views.blog import blog_bp
    app.register_blueprint(blog_bp)

    # 注册 admin 蓝图
    from flaskblog.views.admin import admin_bp
    app.register_blueprint(admin_bp,url_prefix = '/admin')

    # 注册 auth 蓝图
    from flaskblog.views.auth import auth_bp
    app.register_blueprint(auth_bp,url_prefix = '/auth')


def register_extensions(app):
    """初始化app"""
    from flaskblog.extensions import db, login_manager, sitemap, migrate
    db.init_app(app)
    login_manager.init_app(app)
    sitemap.init_app(app)
    migrate.init_app(app, db=db)



def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building Bluelog, just for you."""
        from flaskblog.models import User, Tag, Category, Article
        click.echo('Initializing the database...')
        db.create_all()

        user = User.query.first()
        if user is not None:
            click.echo('The administrator already exists, updating...')
            user.username = username
            user.password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            # user = User(username=username,email
            #
            # )
            # admin.set_password(password)
            # db.session.add(admin)
    #
    #     category = Category.query.first()
    #     if category is None:
    #         click.echo('Creating the default category...')
    #         category = Category(name='Default')
    #         db.session.add(category)
    #
    #     db.session.commit()
    #     click.echo('Done.')
    #
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--tags', default=50, help='Quantity of posts, default is 50.')
    @click.option('--article', default=500, help='Quantity of comments, default is 500.')
    def forge(category, tags, article):
        """Generate fake data."""
        from flaskblog.fakes import fake_user,fake_categories,fake_tags,fake_article

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_user()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)
        #
        click.echo('Generating %d tags...' % tags)
        fake_tags(tags)

        click.echo('Generating %d article...' % article)
        fake_article(article)
    #
    #     click.echo('Generating links...')
    #     fake_links()
    #
        click.echo('Done.')


def register_template_context(app):
    from flask_login import current_user
    @app.context_processor
    def make_template_context():
        ''' 上下文处理器, 返回的字典可以在全部模板中使用'''
        Categories = Category.query.order_by(Category.name).all()
        tags = Tag.query.order_by(Tag.name).all()
        tag_color = ["badge-primary", "badge-secondary", "badge-success", "badge-danger"]
        return dict(current_user=current_user,categores = Categories,tags = tags,tag_color=tag_color) # TODO: 暂且先返回current_user,后面再改.
