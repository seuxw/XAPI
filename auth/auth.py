# -*- coding: utf-8 -*-
# JWT 身份验证模块

import jwt

AUTHORIZATION_HEADER = 'Authorization'
AUTHORIZATION_METHOD = 'Bearer'

# TODO: 临时密码
SECRET_KEY = "WGlYaV9hbmRfRG9uZ0Rvbmc="

JWT_OPTIONS = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_iss': True,
    'verify_aud': False
}

INFO = {"author": "smallwei", "version": "2.1"}


def is_valid_header(parts):
    """header 验证."""
    return True if parts[0] == AUTHORIZATION_METHOD and len(parts) == 2 else False


# 用户类别 0-普通 10-VIP 20-管理 30-超级管理
COMMON = 0
VIP = 10
ADMIN = 20
MASTER = 30


def jwtauth(user=ADMIN):
    """JWT 身份验证.

    Args:
        user: 用户类别：0 - COMMON - 普通，
                      10 - VIP - VIP，
                      20 - ADMIN - 管理，
                      30 - MASTER - 超级管理
    """
    def decorator(handler_class):
        def wrap_execute(handler_execute):
            def require_auth(handler, kwargs):

                auth = handler.request.headers.get(AUTHORIZATION_HEADER)
                if not auth:
                    handler.INFO = INFO
                    return handler.write_error_f(4012)

                auth_parts = auth.split()
                if not is_valid_header(auth_parts):
                    handler.INFO = INFO
                    return handler.write_error_f(4011)

                token = auth_parts[1]
                try:
                    jwt.decode(
                        token,
                        SECRET_KEY,
                        options=JWT_OPTIONS,
                        algorithms='HS256'
                    )
                except Exception as err:
                    handler.INFO = INFO
                    return handler.write_error_f(4011)
                # TODO:
                print(user)
                return True

            def _execute(self, transforms, *args, **kwargs):
                try:
                    require_auth(self, kwargs)
                except Exception:
                    return False
                return handler_execute(self, transforms, *args, **kwargs)
            return _execute

        handler_class._execute = wrap_execute(handler_class._execute)
        return handler_class
    return decorator
