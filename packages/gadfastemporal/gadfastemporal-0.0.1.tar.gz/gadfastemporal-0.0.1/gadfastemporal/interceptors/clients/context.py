from __future__ import annotations

import contextlib
import contextvars
import typing

import temporalio.activity
import temporalio.api.common.v1
import temporalio.client
import temporalio.converter
import temporalio.worker
import temporalio.workflow


class _InputWithHeaders(typing.Protocol):
    headers: typing.MutableMapping[str, temporalio.api.common.v1.Payload]


def set_header_from_context(
    input: _InputWithHeaders,
    contexts: list[contextvars.ContextVar] | None,
    payload_converter: temporalio.converter.PayloadConverter,
) -> None:
    headers = dict(input.headers)

    for context in contexts:
        if value := context.get(None):
            payload = payload_converter.to_payload(value)
            headers[context.name] = payload

    input.headers = headers


@contextlib.contextmanager
def context_from_header(
    input: _InputWithHeaders,
    contexts: list[contextvars.ContextVar] | None,
    payload_converter: temporalio.converter.PayloadConverter,
):
    tokens = []

    if contexts and input.headers:
        for context in contexts:
            if context.name in input.headers:
                value = payload_converter.from_payload(input.headers[context.name], dict)
                token = context.set(value)
                tokens.append((context, token))

    try:
        yield
    finally:
        for context, token in tokens:
            context.reset(token)


class ContextPropagationInterceptor(temporalio.client.Interceptor, temporalio.worker.Interceptor):
    def __init__(
        self,
        contexts: list[contextvars.ContextVar] | None = None,
        payload_converter: temporalio.converter.PayloadConverter = temporalio.converter.default().payload_converter,
    ) -> None:
        self._contexts = contexts
        self._payload_converter = payload_converter

    def intercept_client(self, next: temporalio.client.OutboundInterceptor) -> temporalio.client.OutboundInterceptor:
        return _ContextPropagationClientOutboundInterceptor(next, self._contexts, self._payload_converter)

    def intercept_activity(
        self, next: temporalio.worker.ActivityInboundInterceptor
    ) -> temporalio.worker.ActivityInboundInterceptor:
        return _ContextPropagationActivityInboundInterceptor(next, self._contexts, self._payload_converter)

    def workflow_interceptor_class(
        self, input: temporalio.worker.WorkflowInterceptorClassInput
    ) -> typing.Type[temporalio.worker.WorkflowInboundInterceptor]:
        contexts = self._contexts
        payload_converter = self._payload_converter

        class WorkflowInterceptor(_ContextPropagationWorkflowInboundInterceptor):
            def __init__(self, next_interceptor: temporalio.worker.WorkflowInboundInterceptor):
                super().__init__(next_interceptor, contexts, payload_converter)

        return WorkflowInterceptor


class _ContextPropagationClientOutboundInterceptor(temporalio.client.OutboundInterceptor):
    def __init__(
        self,
        next: temporalio.client.OutboundInterceptor,
        contexts: list[contextvars.ContextVar] | None,
        payload_converter: temporalio.converter.PayloadConverter,
    ) -> None:
        super().__init__(next)
        self._contexts = contexts
        self._payload_converter = payload_converter

    async def start_workflow(
        self, input: temporalio.client.StartWorkflowInput
    ) -> temporalio.client.WorkflowHandle[typing.Any, typing.Any]:
        set_header_from_context(input, self._contexts, self._payload_converter)
        return await super().start_workflow(input)

    async def query_workflow(self, input: temporalio.client.QueryWorkflowInput) -> typing.Any:
        set_header_from_context(input, self._contexts, self._payload_converter)
        return await super().query_workflow(input)

    async def signal_workflow(self, input: temporalio.client.SignalWorkflowInput) -> None:
        set_header_from_context(input, self._contexts, self._payload_converter)
        await super().signal_workflow(input)

    async def start_workflow_update(
        self, input: temporalio.client.StartWorkflowUpdateInput
    ) -> temporalio.client.WorkflowUpdateHandle[typing.Any]:
        set_header_from_context(input, self._contexts, self._payload_converter)
        return await super().start_workflow_update(input)


class _ContextPropagationActivityInboundInterceptor(temporalio.worker.ActivityInboundInterceptor):
    def __init__(
        self,
        next: temporalio.worker.ActivityInboundInterceptor,
        contexts: list[contextvars.ContextVar] | None,
        payload_converter: temporalio.converter.PayloadConverter,
    ) -> None:
        super().__init__(next)
        self._contexts = contexts
        self._payload_converter = payload_converter

    async def execute_activity(self, input: temporalio.worker.ExecuteActivityInput) -> typing.Any:
        with context_from_header(input, self._contexts, self._payload_converter):
            return await self.next.execute_activity(input)


class _ContextPropagationWorkflowInboundInterceptor(temporalio.worker.WorkflowInboundInterceptor):
    def __init__(
        self,
        next: temporalio.worker.WorkflowInboundInterceptor,
        contexts: list[contextvars.ContextVar] | None,
        payload_converter: temporalio.converter.PayloadConverter,
    ) -> None:
        super().__init__(next)
        self._contexts = contexts
        self._payload_converter = payload_converter

    def init(self, outbound: temporalio.worker.WorkflowOutboundInterceptor) -> None:
        self.next.init(
            _ContextPropagationWorkflowOutboundInterceptor(outbound, self._payload_converter, self._contexts)
        )

    async def execute_workflow(self, input: temporalio.worker.ExecuteWorkflowInput) -> typing.Any:
        with context_from_header(input, self._contexts, self._payload_converter):
            return await self.next.execute_workflow(input)

    async def handle_signal(self, input: temporalio.worker.HandleSignalInput) -> None:
        with context_from_header(input, self._contexts, self._payload_converter):
            return await self.next.handle_signal(input)

    async def handle_query(self, input: temporalio.worker.HandleQueryInput) -> typing.Any:
        with context_from_header(input, self._contexts, self._payload_converter):
            return await self.next.handle_query(input)

    async def handle_update_handler(self, input: temporalio.worker.HandleUpdateInput) -> typing.Any:
        with context_from_header(input, self._contexts, self._payload_converter):
            return await self.next.handle_update_handler(input)


class _ContextPropagationWorkflowOutboundInterceptor(temporalio.worker.WorkflowOutboundInterceptor):
    def __init__(
        self,
        next: temporalio.worker.WorkflowOutboundInterceptor,
        payload_converter: temporalio.converter.PayloadConverter,
        contexts: list[contextvars.ContextVar] | None,
    ) -> None:
        super().__init__(next)
        self._contexts = contexts
        self._payload_converter = payload_converter

    async def signal_child_workflow(self, input: temporalio.worker.SignalChildWorkflowInput) -> None:
        set_header_from_context(input, self._contexts, self._payload_converter)
        return await self.next.signal_child_workflow(input)

    async def signal_external_workflow(self, input: temporalio.worker.SignalExternalWorkflowInput) -> None:
        set_header_from_context(input, self._contexts, self._payload_converter)
        return await self.next.signal_external_workflow(input)

    def start_activity(self, input: temporalio.workflow.StartActivityInput) -> temporalio.workflow.ActivityHandle:
        set_header_from_context(input, self._contexts, self._payload_converter)
        return self.next.start_activity(input)

    async def start_child_workflow(
        self, input: temporalio.worker.StartChildWorkflowInput
    ) -> temporalio.workflow.ChildWorkflowHandle:
        set_header_from_context(input, self._contexts, self._payload_converter)
        return await self.next.start_child_workflow(input)

    def start_local_activity(
        self, input: temporalio.workflow.StartLocalActivityInput
    ) -> temporalio.workflow.ActivityHandle:
        set_header_from_context(input, self._contexts, self._payload_converter)
        return self.next.start_local_activity(input)
