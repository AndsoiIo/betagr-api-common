from functools import wraps

from sanic.response import json
from sqlalchemy import select, and_, desc, asc

from ..rest_client.base_client_sso import BaseClientSSO
from ..utils.utils import check_validation_params
from ..utils.constants import _OPERATIONS

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


def filter_data(table_name):
    def decorator(f):
        @wraps(f)
        async def decorated_function(self, request, *args, **kwargs):
            query_params = request.raw_args
            valid_column = dict(table_name.columns)
            field_params = query_params.get("fields").split(", ") if query_params.get("fields") else None
            where_params = [f"{key}:eq:{value}" for key, value in kwargs.items()]
            where_params.extend(query_params.get("where").split(", ")) if query_params.get("where") else None
            order_by_params = query_params.get("order_by")
            order = desc if query_params.get("order") == "desc" else asc
            if not await check_validation_params(valid_column, field_params, order_by_params):
                request["sql_expr"] = select([table_name])
                return await f(self, request, *args, **kwargs)
            if field_params:
                expr = select([table_name.c[field] for field in field_params]).order_by(
                    order(table_name.c[order_by_params]) if order_by_params else None)
            else:
                expr = select([table_name]).order_by(
                    order(table_name.c[order_by_params]) if order_by_params else None)

            filter_by = []
            if where_params:
                for where in where_params:
                    column, operation, value = where.split(":")

                    if column not in valid_column:
                        request["sql_expr"] = expr
                        return await f(self, request, *args, **kwargs)

                    operation = _OPERATIONS.get(operation)
                    if operation:
                        filter_by.append(operation(table_name.c[column],  value))

                expr = expr.where(and_(by for by in filter_by))
            request["sql_expr"] = expr
            return await f(self, request, *args, **kwargs)
        return decorated_function
    return decorator
