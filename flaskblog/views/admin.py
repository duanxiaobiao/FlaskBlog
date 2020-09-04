import os
from datetime import datetime

from flask import Blueprint, render_template, request, current_app, url_for, jsonify, send_from_directory

from flaskblog.extensions import db
from flaskblog.forms import ArticleForm
from flaskblog.models import Picture
from flaskblog.utils import allowed_file, upload_file_qiniu

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login')
def login():

    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():

    return render_template('admin/login.html')

@admin_bp.route('/')
def index():
    return render_template('admin/index.html')


@admin_bp.route('/article/write',methods = ["GET","POST"])
def write():
    form = ArticleForm()
    if form.validate_on_submit():
        pass

    return render_template('admin/write.html', form=form)

@admin_bp.route('/imagehosting',methods=["GET","POST"])
def image_hosting():
    """
    图床
    """
    # from app.util import file_list_qiniu
    # imgs = file_list_qiniu()
    page = request.args.get('page',1, type=int)
    imgs = Picture.query.order_by(Picture.id.desc()). \
        paginate(page, per_page=20, error_out=False)
    return render_template('admin/image_hosting.html',imgs = imgs)

@admin_bp.route('/upload',methods=['POST'])
def upload():
    file = request.files.get("file")
    if not allowed_file(file.filename):
        res={
            'code':0,
            'msg':'图片格式异常'
        }
    else:
        url_path = ''
        upload_type = current_app.config.get('H3BLOG_UPLOAD_TYPE')
        ex=os.path.splitext(file.filename)[1]
        filename=datetime.now().strftime('%Y%m%d%H%M%S')+ex
        if upload_type is None or upload_type == '' or upload_type == 'local':
            file.save(os.path.join(current_app.config['BLOG_UPLOAD_PATH'],filename))
            url_path = url_for('admin.get_image',filename=filename)
        elif upload_type == 'qiniu':
            try:
                qiniu_cdn_url = current_app.config.get('QINIU_CDN_URL')
                url_path = qiniu_cdn_url + upload_file_qiniu(file.read(),filename)
            except Exception as e:
                return jsonify({'success':0,'message':'上传图片异常'})
        #返回
        pic = Picture(name = file.filename if len(file.filename)< 32 else filename,url = url_path)
        db.session.add(pic)
        res={
            'code':1,
            'msg':u'图片上传成功',
            'url': url_path
        }
    return jsonify(res)

@admin_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['BLOG_UPLOAD_PATH'], filename)

