# -*- coding: utf-8 -*-
"""
    Created by 亥虫 on 2019/5/12
"""
from functools import wraps

from flask import Markup, flash, url_for, redirect, abort
from flask_login import current_user


def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            message = Markup(
                '请先确认你的账号'
                '没有收到邮件？'
                '<a class="alert-link" href="%s">重新发送确认邮件</a>' % url_for('auth.resend_confirm_email'))
            flash(message, 'warning')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return decorated_function


def permission_required(permission_name):
    def decorator(func):
        @wraps(func)
        def decorator_function(*args, **kwargs):
            if not current_user.can(permission_name):
                abort(403)
            return func(*args, **kwargs)
        return decorator_function
    return decorator


def admin_required(func):
    return permission_required('ADMINISTER')(func)