from functools import wraps

from rest_client.base_client_sso import BaseClientSSO

client = BaseClientSSO()

def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            response = await client.check_auth()
            if response.status == 200:
                return await f(request, *args, **kwargs)
            return response
        return decorated_function
    return decorator


def authorized_and_user_has(permission):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            response = await client.check_auth_and_user_has(json={"permission": permission})
            if response.status == 200:
                return await f(request, *args, **kwargs)
            return response
        return decorated_function
    return decorator


def authorized_and_user_in_group(group):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            response = await client.check_auth_and_user_in_group(json={"group": group})
            if response.status == 200:
                return await f(request, *args, **kwargs)
            return response
        return decorated_function
    return decorator
