# -*- coding: utf-8 -*-
"""
    Created by 亥虫 on 2019/5/23
"""
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Regexp, Optional, ValidationError, Email, EqualTo

from albumy.models import User


class EditProfileForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired(), Length(1, 30)])
    username = StringField('账号', validators=[DataRequired(), Length(1, 20), Regexp('^[a-zA-Z0-9]*$',
                                                                                   message='账号只能由字母或者数字组成')])
    website = StringField('站点', validators=[Optional(), Length(0, 255)])
    location = StringField('城市', validators=[Optional(), Length(0, 50)])
    bio = TextAreaField('简介', validators=[Optional(), Length(0, 120)])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('该账号已被使用')


class UploadAvatarForm(FlaskForm):
    image = FileField('上传文件', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], '只能上传后缀名为 .jpg 或者 .png 格式的文件')])
    submit = SubmitField('提交')


class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('剪切并更新')


class ChangeEmailForm(FlaskForm):
    email = StringField('新的邮箱', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('该邮箱已被使用')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧的密码', validators=[DataRequired()])
    password = PasswordField('新的密码', validators=[
        DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('提交')


class NotificationSettingForm(FlaskForm):
    receive_comment_notification = BooleanField('新的评论')
    receive_follow_notification = BooleanField('新的关注')
    receive_collect_notification = BooleanField('新的收藏')
    submit = SubmitField()


class PrivacySettingForm(FlaskForm):
    public_collections = BooleanField('公开我的收藏')
    submit = SubmitField()


class DeleteAccountForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField()

    def validate_username(self, field):
        if field.data != current_user.username:
            raise ValidationError('账号错误')