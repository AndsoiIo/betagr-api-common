from ..rest_client.base_client_camunda import BaseClientCamunda

client_camunda = BaseClientCamunda()


class Camunda:
    workflow_steps = {
        "New": "action",
        "Moderated": "action",
        "Approved": "approved",
    }

    @classmethod
    async def get_process_definition_id(cls, name_process_definition):
        resp = await client_camunda.get_process_definition(name_process_definition)
        process_definition_list = resp.json
        process_definition_id = process_definition_list[0]["id"] if process_definition_list else None

        if not process_definition_id:
            raise CamundaException(f"Can not init process. "
                                   f"'{name_process_definition}' process definition does not exists")

        return process_definition_id

    @classmethod
    async def start_process(cls, process_definition_id, business_key):
        resp = await client_camunda.process_definition_start(process_definition_id, business_key)

        if resp.status != 200:
            raise CamundaException("Can not start process instance")

        resp_json = resp.json
        return resp_json["id"]

    @classmethod
    async def _get_current_task(cls, process_instance_id):
        resp = await client_camunda.get_current_task(process_instance_id)
        task = resp.json
        return task[0] if task else None

    @classmethod
    async def _get_process_instance(cls, business_key):
        resp = await client_camunda.get_process_instance(business_key)
        process_instance = resp.json
        return process_instance[0] if process_instance else None

    @classmethod
    async def task_complete(cls, business_key, name, value):
        process_instance = await cls._get_process_instance(business_key)

        if not process_instance:
            raise CamundaException("Business key not valid")

        process_instance_id = process_instance["id"]
        current_task = await cls._get_current_task(process_instance_id)

        if not current_task:
            raise CamundaException("Can not task complete. Task does not exists")

        if name != current_task["name"]:
            raise CamundaException(f"Can not task complete. Task '{name}' not match with name current task")

        action = cls.workflow_steps[name]
        resp = await client_camunda.task_complete(current_task["id"], action, value)

        if resp.status != 204:
            raise CamundaException("Can not task complete. Not valid value")


class CamundaException(Exception):
    pass
