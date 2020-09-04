from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_sitemap import Sitemap
from flask_migrate import Migrate


bootstrap = Bootstrap()
db = SQLAlchemy()
sitemap = Sitemap()
login_manager = LoginManager()
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    from flaskblog.models import User
    print(user_id,"==================")
    user = User.query.get(int(user_id))
    return user


login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'
