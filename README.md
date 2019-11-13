# BetAgr-common - base async api-clients for betagr-project wrote with aiohttp

A set of tools, utilities and base async api-classes for maintaining the infrastructure of betagr-project services.

### Requirements

* python>=3.6
* aiohttp>=3.6

### Usage

```
pip install betagr-common

# or only for user
python -m pip install --user betagr-common

# or for pipenv
pipenv install betagr-common
```

BetAgr-common ships with two base api-classes: BaseClient and BaseClientSSO.

##### BaseClient

It is a base class provides a basic REST API methods which are simple wrapper over a aiohttp.request.
Сlass also implements basic logging of client requests and handling cookies within one client, since the connection session exists only during one request.

Api-clients of each  services should be inherited from the BaseClient.

```python
from common.rest_client import BaseClient

class BakeryClient(BaseClient):
    def __init__(self, headers):
        super().__init__(host='www.some-bakery.com', port=8000, headers=headers)
        self._api_uri = {
            'bake_bread' : 'api/bake-bread',
        }

    async def bake_bread(self, bread_flour='first-grade'):
        body = {'flour': bread_flour}
        api_uri = self._api_uri['bake-bread']

        return await super().post(api_uri, body=body, cookies=self._cookies)
```

```python
import asyncio
import BakeryClient

db_orders = {'John Doe': {'flour': 'first-grade'},
                     'Anderson': {'flour': 'second-grade'}}

async def main():
    async for client in db_orders:
        custom_headers = {'Content-Type': 'application/json'}

        bakery_client = BakeryClient(custom_headers)
        
        bread_flour_type = db_orders[client].get('flour')            

        async with await bakery_client.bake_bread(bread_flour_type) as resp:
            assert resp.status == 200    # bread was bake!
                        

loop = asyncio.get_event_loop()
loop.run_until_complete(main())  
```

##### BaseClientSSO
Api abstraction for sso-client with the release of basic methods:
* sign_up
* sign_in
* sign_out
* reset_password

``BaseClientSSO._api_uri`` should be used to represent method and relevant api path.
For default it looks like:
```python
BaseClientSSO._api_uri = {
            'sign_up': 'sign-up',
            'sign_in': 'sign-in',
            'sign_out': 'sign-out',
            'reset_password': 'reset-password',
            }
```

Use ``sef._api_uri.update({'my_new_method': 'api_uri_used_in_method'})``  - it is some kind of bookmark that makes it easy to maintain your inherited classes.

```python
import os
import asyncio
from common.rest_client import BaseClientSSO


async def main():
    host = os.getenv('SSO_API_HOST')
    port = os.getenv('SSO_API_PORT')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    sso_client = BaseClientSSO(host, port, headers)

    body = {'username': 'john doe',
            'password': 'qwerty'}

    async with await sso_client.sign_up(body) as response:
        print(response)

    body = {'username': 'john doe',
            'password': 'qwerty'}

    async with await sso_client.sign_in(body) as response:
        print(response)

    body = {'username': 'john doe',
            'old_password': 'qwerty',
            'new_password': 'qwerty'}

    async with await sso_client.reset_password(body) as response:
        print(response)

    async with await sso_client.sign_out() as response:
        print(response)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

```
Environment variables are used to determine url/connection parameters in base classes:

|            env variable         |         value         |
|               ---               |          ---          |
| COMMON_API_CLIENT_LOGGING_LEVEL |           40          |

see numeric represents logging level here: https://docs.python.org/3/library/logging.html#logging-levels
