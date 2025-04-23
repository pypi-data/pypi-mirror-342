import contextvars
import json
import typing

import temporalio.client

from gadfastemporal import policies
from gadfastemporal.workflows import Workflow


class Executor:
    def __init__(
        self,
        client: temporalio.client.Client,
        task_queue: str,
        search_attributes: typing.List[contextvars.ContextVar] | None = None,
    ) -> None:
        self._client = client
        self._task_queue = task_queue
        self._search_attributes = search_attributes or []

    def search_attributes(self) -> dict[str, list]:
        search_attributes = {}

        for context in self._search_attributes:
            if value := context.get(None):
                for k, v in value.items():
                    search_attributes[k] = [json.dumps(v)]

        return search_attributes

    async def sync(
        self,
        workflow: typing.Type[Workflow],
        *args: typing.Any,
        policy: dict | None = None,
    ) -> typing.Any:
        return await self._client.execute_workflow(
            workflow=workflow.run,
            args=list(args),
            id=workflow.id(args),
            task_queue=self._task_queue,
            search_attributes=self.search_attributes(),
            **policy if policy else policies.workflows.once(),
        )

    async def polling(
        self,
        workflow: typing.Type[Workflow],
        *args: typing.Any,
        policy: dict | None = None,
    ) -> temporalio.client.WorkflowHandle:
        return await self._client.start_workflow(
            workflow=workflow.run,
            args=list(args),
            id=workflow.id(args),
            task_queue=self._task_queue,
            search_attributes=self.search_attributes(),
            **policy if policy else policies.workflows.once(),
        )


__all__ = ["Executor"]
