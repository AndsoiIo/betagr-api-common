import os

from common.rest_client.base_client import BaseClient


class BaseClientBettingData(BaseClient):

    _host = os.getenv('BETTING_DATA_API_HOST')
    _port = int(os.getenv('BETTING_DATA_API_PORT'))

    async def get_teams(self, link_id=None):
        url = '/teams'
        if link_id:
            url = f'{url}?link_id={link_id}'
        response = await self.get(api_uri=url)
        teams = response.json
        return teams

    async def put_teams(self, link_id=None):
        url = '/teams'
        if link_id:
            url = f'{url}?link_id={link_id}'
        response = await self.put(api_uri=url)
        return response

    async def change_status_team(self, team_id, json):
        url = '/team/{team_id}'.format(team_id=team_id)
        if not isinstance(json, dict):
            json = {}
        response = await self.patch(api_uri=url, data=json)
        return response

    async def get_real_teams(self):
        url = '/real-teams'
        response = await self.get(api_uri=url)
        real_teams = response.json
        return real_teams

    async def put_real_teams(self):
        url = '/real-teams'
        response = await self.put(api_uri=url)
        return response
