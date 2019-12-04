from functools import wraps

from sanic.response import json
from ..rest_client.base_client_sso import BaseClientSSO

client = BaseClientSSO()


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            response = await client.check_auth(cookies=request.cookies)
            if response.status == 200:
                return await f(request, *args, **kwargs)
            return json(response.json, response.status)
        return decorated_function
    return decorator


def authorized_and_user_has(permission):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            response = await client.check_auth_and_user_has(cookies=request.cookies,
                                                            json={"permission": permission})
            if response.status == 200:
                return await f(request, *args, **kwargs)
            return json(response.json, response.status)
        return decorated_function
    return decorator


def authorized_and_user_in_group(group):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            response = await client.check_auth_and_user_in_group(cookies=request.cookies,
                                                                 json={"group": group})
            if response.status == 200:
                return await f(request, *args, **kwargs)
            return json(response.json, response.status)
        return decorated_function
    return decorator
