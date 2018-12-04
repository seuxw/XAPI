# -*- coding: utf-8 -*-
# 此工具用于手动对用户权限进行提升

# TODO: 临时密码
SECRET_KEY = "WGlYaV9hbmRfRG9uZ0Rvbmc="


def token_decode(token):
    jwt.decode(
        token,
        SECRET_KEY,
        options=JWT_OPTIONS,
        algorithms='HS256'
    )


def token_encode():
    token = jwt.encode(
        payload={
            'iss': "xapi.seuxw.cn",
            'aud': self.get_argument("tk"),
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=self.TIMEOUT)
        },
        key=SECRET_KEY,
        algorithm='HS256'
    )
    response = {'token': token.decode('ascii')}
