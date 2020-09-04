# -*- coding: utf-8 -*-
import os
import sys
import hashlib

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or hashlib.new(name='md5', string='duanxiaobiao').hexdigest()

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('H3BLOG Admin', MAIL_USERNAME)

    BLOG_TITLE = os.getenv('H3BLOG_TITLE', '彪哥博客')

    BLOG_KEYWORDS = os.getenv('BLOG_KEYWORDS', 'python,flask,个人博客')
    BLOG_DESCRIPTION = os.getenv('BLOG_DESCRIPTION',
                                   'FLASK学习搭建的网站，正在初步搭建中.... ')
    BLOG_EMAIL = os.getenv('BLOG_EMAIL')
    BLOG_POST_PER_PAGE = 10
    BLOG_MANAGE_POST_PER_PAGE = 15
    BLOG_COMMENT_PER_PAGE = 15
    BLOG_SLOW_QUERY_THRESHOLD = 1
    BLOG_REGISTER_INVITECODE = True  # 是否开启邀请码注册

    BLOG_UPLOAD_TYPE = os.getenv('BLOG_UPLOAD_TYPE', '')  # 默认本地上传
    BLOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    BLOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'webp']

    MAX_CONTENT_LENGTH = 32 * 1024 * 1024


    QINIU_BUCKET_NAME = os.getenv('QINIU_BUCKET_NAME', 'blog')
    QINIU_ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY', 'key123')
    QINIU_SECRET_KEY = os.getenv('QINIU_SECRET_KEY', 'secret456')

    BAIDU_PUSH_TOKEN = os.getenv('BAIDU_PUSH_TOKEN')  # 主动推送给百度链接，token是在搜索资源平台申请的推送用的准入密钥

    SITEMAP_URL_SCHEME = os.getenv('SITEMAP_URL_SCHEME', 'http')
    SITEMAP_MAX_URL_COUNT = os.getenv('SITEMAP_MAX_URL_COUNT', 100000)


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

if __name__ == "__main__":
    pass









