# -*- coding: utf-8 -*-
"""
    Created by 亥虫 on 2019/5/8
"""
from flask_avatars import Avatars
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager, AnonymousUserMixin
from flask_dropzone import Dropzone
from flask_whooshee import Whooshee
from flask_wtf import CSRFProtect


db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
dropzone = Dropzone()
csrf = CSRFProtect()
moment = Moment()
whooshee = Whooshee()
avatars = Avatars()
csrf = CSRFProtect()
bootstrap = Bootstrap()


@login_manager.user_loader
def load_user(user_id):
    from albumy.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'

login_manager.refresh_view = 'auth.re_authenticate'
# login_manager.needs_refresh_message = 'Your custom message'
login_manager.needs_refresh_message_category = 'warning'
login_manager.needs_refresh_message = u'为了保护你的账户安全，请重新登录。'


class Guest(AnonymousUserMixin):
    def can(self, permission_name):
        return False

    @property
    def is_admin(self):
        return False


login_manager.anonymous_user = Guest