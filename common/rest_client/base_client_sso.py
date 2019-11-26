import os
import logging

from common.utils import client_response as ClientResponse
from common.rest_client.base_client import BaseClient


class BaseClientSSO(BaseClient):
    """Base api client that describes full standard api for SSO service."""

    _host = os.getenv('SSO_API_HOST')
    _port = int(os.getenv('SSO_API_PORT'))

    def __init__(self, headers=None):
        super().__init__(headers=headers)

    async def sign_up(self, body):
        url = '/sign-up'
        return await self.post(url, body=body)

    async def sign_in(self, body):
        url = '/sign-in'
        return await self.post(url, body=body)

    async def sign_out(self):
        url = '/sign-out'
        return await self.post(url)

    async def reset_password(self, body):
        url = '/reset-password'
        return await self.patch(url, body=body)

    async def is_permission_granted(self, cookies: dict):
        url = '/'
        if not cookies.get('session'):
            # eliminates a redundant requests for sso server
            logging.warning('The request does not contain a session field in cookies')
            return ClientResponse(status=401, reason="Unauthorized",
                                  headers={'Content-Type': 'application/json'},
                                  json={}, raw_content={})

        return await self.get(api_uri=url, cookies=cookies)
