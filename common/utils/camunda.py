import aiohttp

from rest_client.exceptions import CamundaAPIException


class CamundaAPI:
    base_url = "http://localhost:8085/engine-rest/engine/default"
    process_instance_id = None
    current_task = None
    workflow_steps = {
        "Request": "action",
        "New": "action",
        "Moderated": "action",
        "Approved": "approved",
    }

    @classmethod
    async def init(cls, name_process_definition):
        process_def_url = await cls._url(f"process-definition?name={name_process_definition}")
        async with aiohttp.ClientSession() as session:
            async with session.get(process_def_url) as resp:
                process_definition_list = await resp.json()
                process_definition_id = process_definition_list[0]["id"] if process_definition_list else None

                if not process_definition_id:
                    raise CamundaAPIException(f"Can not init process. "
                                              f"'{name_process_definition}' process definition does not exists")

                await cls.start_process(process_definition_id)

    @classmethod
    async def _url(cls, resource):
        return f"{cls.base_url}/{resource}"

    @classmethod
    async def start_process(cls, process_definition_id):
        start_process_url = await cls._url(f"process-definition/{process_definition_id}/start")
        async with aiohttp.ClientSession(headers={"Content-Type": "application/json"}) as session:
            async with session.post(start_process_url, ) as resp:

                if resp.status != 200:
                    raise CamundaAPIException("Can not start process instance")

                resp_json = await resp.json()
                cls.process_instance_id = resp_json["id"]
                await cls.set_task()

    @classmethod
    async def set_task(cls):
        task_url = await cls._url(f"task?processInstanceId={cls.process_instance_id}")

        async with aiohttp.ClientSession() as session:
            async with session.get(task_url) as resp:
                task = await resp.json()
                if task:
                    cls.current_task = task[0]
                else:
                    cls.current_task = None

    @classmethod
    async def task_complete(cls, name, approved):
        if not cls.current_task:
            raise CamundaAPIException("Can not task complete. Task does not exists")

        task = cls.current_task
        if name != task["name"]:
            raise CamundaAPIException(f"Can not task complete. Task '{name}' not match with name current task")

        complete_task_url = await cls._url(f"task/{task['id']}/complete")
        action = cls.workflow_steps[name]

        req_body = {
            "variables": {
                action: {
                    "value": approved,
                    "type": "Boolean"
                }
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(complete_task_url, json=req_body) as resp:
                if resp.status != 204:
                    raise CamundaAPIException("Can not task complete. Not valid value")
                await cls.set_task()
