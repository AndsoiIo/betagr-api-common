import os

from common.rest_client.base_client import BaseClient


class BaseClientSSO(BaseClient):
    """Base api client that describes full standard api for SSO service."""

    _host = os.getenv('SSO_API_HOST')
    _port = int(os.getenv('SSO_API_PORT'))

    def __init__(self, headers=None):
        super().__init__(headers=headers)

    async def sign_up(self, json):
        url = '/sign-up'
        return await self.post(url, data=json)

    async def sign_in(self, json):
        url = '/sign-in'
        return await self.post(url, data=json)

    async def sign_out(self):
        url = '/sign-out'
        return await self.post(url)

    async def reset_password(self, json):
        url = '/reset-password'
        return await self.patch(url, data=json)

    async def check_auth(self):
        url = '/check-auth'
        return await self.post(url)

    async def check_auth_and_user_in_group(self, json):
        url = '/check-group'
        return await self.post(url, data=json)

    async def check_auth_and_user_has(self, json):
        url = '/check-permission'
        return await self.post(url, data=json)

    async def check_auth_and_get_permissions(self):
        url = '/get-permissions'
        return await self.get(url)
