# -*- coding: utf-8 -*-
"""
    Created by 亥虫 on 2019/5/24
"""
import os
import random

from PIL import Image
from faker import Faker
from flask import current_app
from sqlalchemy.exc import IntegrityError

from albumy.extensions import db
from albumy.models import User, Notification, Tag, Photo, Comment

fake = Faker(locale='zh-cn')


def fake_admin():
    admin = User(
        name='HaiChong',
        username='HaiChong',
        email='1243726062@qq.com',
        bio=fake.sentence(),
        website='www.haichong.xyz',
        confirmed=True)

    admin.set_password('123456')
    notification = Notification(message='Hello, welcome to Albumy.', receiver=admin)
    db.session.add(notification)
    db.session.add(admin)
    db.session.commit()


def fake_user(count=10):
    for i in range(count):
        user = User(
            name=fake.name(),
            confirmed=True,
            username=fake.user_name(),
            bio=fake.sentence(),
            location=fake.city(),
            website=fake.url(),
            member_since=fake.date_this_decade(),
            email=fake.email()
        )
        user.set_password('123456')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_follow(count=30):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        user.follow(User.query.get(random.randint(1, User.query.count())))
    db.session.commit()


def fake_tag(count=20):
    for i in range(count):
        tag = Tag(name=fake.word())
        db.session.add(tag)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_photo(count=30):
    upload_path = current_app.config['ALBUMY_UPLOAD_PATH']
    for i in range(count):
        filename = 'random_%d.jpg' % i
        print(filename)

        r = lambda: random.randint(128, 255)
        img = Image.new(mode='RGB', size=(800, 800), color=(r(), r(), r()))
        img.save(os.path.join(upload_path, filename))

        photo = Photo(
            description=fake.text(),
            filename=filename,
            filename_m=filename,
            filename_s=filename,
            author=User.query.get(random.randint(1, User.query.count())),
            timestamp=fake.date_time_this_year()
        )

        # tags
        for j in range(random.randint(1, 5)):
            tag = Tag.query.get(random.randint(1, Tag.query.count()))
            if tag not in photo.tags:
                photo.tags.append(tag)

        db.session.add(photo)
    db.session.commit()


def fake_collect(count=50):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        user.collect(Photo.query.get(random.randint(1, Photo.query.count())))
    db.session.commit()


def fake_comment(count=10):
    for i in range(count):
        comment = Comment(
            author=User.query.get(random.randint(1, User.query.count())),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            photo=Photo.query.get(random.randint(1, Photo.query.count()))
        )
        db.session.add(comment)
    db.session.commit()