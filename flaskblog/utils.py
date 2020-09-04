from functools import wraps

from flask_login import current_user
from flask import abort, current_app


def admin_required(func):
    """ 检查管理员权限 """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_admin():
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator(func)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['BLOG_ALLOWED_IMAGE_EXTENSIONS']


def upload_file_qiniu(inputdata,filename=None):
    from qiniu import Auth, put_data, etag
    access_key = current_app.config.get('QINIU_ACCESS_KEY')
    secret_key = current_app.config.get('QINIU_SECRET_KEY')
    '''
    :param inputdata: bytes类型的数据
    :return: 文件在七牛的上传名字
    '''
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    #要上传的空间
    bucket_name = 'blog'

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name)
    #如果需要对上传的图片命名，就把第二个参数改为需要的名字
    ret1,ret2=put_data(token,filename,data=inputdata)
    print('ret1:',ret1)
    print('ret2:',ret2)

    #判断是否上传成功
    if ret2.status_code!=200:
        raise Exception('文件上传失败')

    return ret1.get('key')
