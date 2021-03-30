import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#############################################################################
############ 配置及初始化 ###############
###########################################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

#################################
### 数据库配置 ############
###############################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app,db)


###########################
#### 登录配置 #######
#########################

login_manager = LoginManager()

# 传递app到login_manager
login_manager.init_app(app)

login_manager.login_view = "users.login"

# 蓝图导入及配置
from MyBookStore.core.views import core
from MyBookStore.users.views import users
from MyBookStore.blog_posts.views import blog_posts
from MyBookStore.error_pages.handlers import error_pages

app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(core)
app.register_blueprint(error_pages)

