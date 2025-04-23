from __future__ import annotations

import asyncio
import contextvars
import typing

import temporalio.client
import temporalio.converter
import temporalio.worker
import temporalio.workflow

from gadfastemporal import executors


class Temporal:
    def __init__(
        self,
        host: str,
        namespace: str,
        task_queue: str,
        workflows: typing.List[typing.Any],
        debug: bool = True,
        worker_interceptors: typing.List[temporalio.worker.Interceptor] = None,
        client_interceptors: typing.List[temporalio.client.Interceptor] = None,
        data_converter: temporalio.converter.DataConverter = temporalio.converter.default(),
        search_attributes: typing.List[contextvars.ContextVar] = None,
    ) -> None:
        self._host = host
        self._namespace = namespace
        self._task_queue = task_queue
        self._activities = [activity for workflow in workflows for activity in workflow.activities()]
        self._workflows = workflows
        self._debug = debug
        self._worker_interceptors = worker_interceptors or []
        self._client_interceptors = client_interceptors or []
        self._data_converter = data_converter
        self._search_attributes = search_attributes or []
        self.client: temporalio.client.Client | None = None
        self.worker: temporalio.worker.Worker | None = None
        self.workflow: executors.workflows.Executor | None = None
        self.activity: executors.activities.Executor | None = None

    def _workflow(self) -> executors.workflows.Executor:
        if self.workflow is None:
            self.workflow = executors.workflows.Executor(self.client, self._task_queue, self._search_attributes)
        return self.workflow

    def _activity(self) -> executors.activities.Executor:
        if self.activity is None:
            self.activity = executors.activities.Executor(self._task_queue)
        return self.activity

    def _worker(self) -> temporalio.worker.Worker:
        if self.worker is None:
            self.worker = temporalio.worker.Worker(
                client=self.client,
                task_queue=self._task_queue,
                activities=self._activities,
                workflows=self._workflows,
                debug_mode=self._debug,
                workflow_runner=temporalio.worker.UnsandboxedWorkflowRunner() if self._debug else None,
                interceptors=self._worker_interceptors,
            )
        return self.worker

    async def _client(self) -> temporalio.client.Client:
        if self.client is None:
            self.client = await temporalio.client.Client.connect(
                self._host,
                namespace=self._namespace,
                data_converter=self._data_converter,
                interceptors=self._client_interceptors,
            )
        return self.client

    async def start(self) -> asyncio.Task:
        await self._client()
        self._worker()
        self._workflow()
        self._activity()
        return asyncio.create_task(self.worker.run())

    async def shutdown(self) -> None:
        if self.worker is not None:
            await self.worker.shutdown()
