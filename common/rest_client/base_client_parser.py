import os

from common.rest_client.base_client import BaseClient


class BaseClientParser(BaseClient):

    _host = os.getenv('PARSER_API_HOST')
    _port = int(os.getenv('PARSER_API_PORT'))

    def __init__(self, headers=None):
        super().__init__(headers=headers)

    async def parse_teams(self, url, cls, elem):
        parser_url = '/parse'
        req_json = {"url": url, "cls": cls, "elem": elem}
        response = await self.post(api_uri=parser_url, data=req_json)
        return response
