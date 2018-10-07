# -*- coding: utf-8 -*-
from django import forms
from captcha.fields import CaptchaField  # 验证码字段


class LoginForm(forms.Form):
    # 登录页面表单验证
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6, max_length=16,
                               error_messages={
                                   'max_length': '密码最多16位',
                                   'min_length': '密码不得少于6位',
                                   'required': '密码字段是不为空',
                               })


class RegisterForm(forms.Form):
    # 注册页面表单验证
    number = forms.IntegerField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})
