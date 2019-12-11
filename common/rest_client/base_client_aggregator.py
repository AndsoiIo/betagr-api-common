import os

from common.rest_client.base_client import BaseClient


class BaseClientAggregator(BaseClient):

    _host = os.getenv('AGGREGATOR_API_HOST')
    _port = int(os.getenv('AGGREGATOR_API_PORT'))

    async def aggregate(self, team=None):
        url = '/aggregate'
        params = {}
        if team:
            params = {'team': team}
        response = await self.get(api_uri=url, params=params)
        return response

    async def aggregate_by_link(self, link_id, team=None):
        url = '/aggregate/{link_id}'.format(link_id=link_id)
        params = {}
        if team:
            params = {'team': team}
        response = await self.get(api_uri=url, params=params)
        return response
