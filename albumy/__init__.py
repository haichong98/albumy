# -*- coding: utf-8 -*-
"""
    Created by 亥虫 on 2019/5/8
"""

import os

import click
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from albumy.blueprints.admin import admin_bp
from albumy.blueprints.ajax import ajax_bp
from albumy.blueprints.main import main_bp
from albumy.blueprints.user import user_bp
from albumy.models import Role
from albumy.settings import config
from albumy.extensions import db, login_manager, mail, dropzone, avatars, whooshee, bootstrap, moment, csrf
from albumy.blueprints.auth import auth_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('albumy')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errorhandlers(app)

    return app


def register_errorhandlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('/errors/405.html'), 405

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 500


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    dropzone.init_app(app)
    avatars.init_app(app)
    whooshee.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(ajax_bp, url_prefix='/ajax')


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='删除之后创建')
    def initdb(drop):
        if drop:
            click.confirm('该选项将会删除数据库，是否继续执行？', abort=True)
            db.drop_all()
            click.echo('删除数据库')
        db.create_all()
        click.echo('初始化数据库')

    @app.cli.command()
    def init():
        """Initialize Albumy."""
        click.echo('初始化数据库')
        db.create_all()

        click.echo('初始化角色与权限')
        Role.init_role()

        click.echo('结束')

    @app.cli.command()
    @click.option('--user', default=10, help='Quantity of users, default is 10.')
    @click.option('--follow', default=30, help='Quantity of follows, default is 30.')
    @click.option('--photo', default=30, help='Quantity of photos, default is 30.')
    @click.option('--tag', default=20, help='Quantity of tags, default is 20.')
    @click.option('--collect', default=50, help='Quantity of collects, default is 50.')
    @click.option('--comment', default=100, help='Quantity of comments, default is 100.')
    def forge(user, follow, photo, tag, collect, comment):
        """Generate fake data."""

        from albumy.fakes import fake_admin, fake_comment, fake_follow, fake_photo, fake_tag, fake_user, fake_collect

        db.drop_all()
        db.create_all()

        click.echo('Initializing the roles and permissions...')
        Role.init_role()
        click.echo('Generating the administrator...')
        fake_admin()
        click.echo('Generating %d users...' % user)
        fake_user(user)
        click.echo('Generating %d follows...' % follow)
        fake_follow(follow)
        click.echo('Generating %d tags...' % tag)
        fake_tag(tag)
        click.echo('Generating %d photos...' % photo)
        fake_photo(photo)
        click.echo('Generating %d collects...' % photo)
        fake_collect(collect)
        click.echo('Generating %d comments...' % comment)
        fake_comment(comment)
        click.echo('Done.')


