# -*- coding: utf-8 -*-
# 此工具用于手动对用户权限进行提升

import datetime

import jwt

from auth import auth


def token_decode(token):
    return jwt.decode(
        token,
        auth.SECRET_KEY,
        options=auth.JWT_OPTIONS,
        algorithms=auth.ALGORITHMS
    )


def token_encode(payload_old, user):
    token = jwt.encode(
        payload={
            'iss': "xapi.seuxw.cn",
            'cnb': payload_old.get("cnb"),
            'usr': user,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=auth.TIMEOUT)
        },
        key=auth.SECRET_KEY,
        algorithm=auth.ALGORITHMS
    )
    return {'token': token.decode('ascii')}


def privilege_escalation():
    token = input("输入要提权 token：")
    try:
        payload = token_decode(token)
        print("Token decode:", payload)
        print("解析正常！")
    except Exception:
        print("解析失败！")
        return
    user = input("输入要提权值 0-普通 10-VIP 20-管理 30-超级管理：")
    token = token_encode(payload, user)
    print("Token encode:", token)
