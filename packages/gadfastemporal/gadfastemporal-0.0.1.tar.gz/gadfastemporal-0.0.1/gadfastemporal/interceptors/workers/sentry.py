import dataclasses
import typing

import temporalio.worker
from temporalio import activity
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    import sentry_sdk


def _set_common_workflow_tags(info: typing.Union[workflow.Info, activity.Info]):
    sentry_sdk.set_tag("temporal.workflow.type", info.workflow_type)
    sentry_sdk.set_tag("temporal.workflow.id", info.workflow_id)


class _SentryActivityInboundInterceptor(temporalio.worker.ActivityInboundInterceptor):
    async def execute_activity(self, input: temporalio.worker.ExecuteActivityInput) -> typing.Any:
        with sentry_sdk.Hub(sentry_sdk.Hub.current):
            sentry_sdk.set_tag("temporal.execution_type", "activity")
            sentry_sdk.set_tag("module", input.fn.__module__ + "." + input.fn.__qualname__)

            activity_info = activity.info()
            _set_common_workflow_tags(activity_info)
            sentry_sdk.set_tag("temporal.activity.id", activity_info.activity_id)
            sentry_sdk.set_tag("temporal.activity.type", activity_info.activity_type)
            sentry_sdk.set_tag("temporal.activity.task_queue", activity_info.task_queue)
            sentry_sdk.set_tag("temporal.workflow.namespace", activity_info.workflow_namespace)
            sentry_sdk.set_tag("temporal.workflow.run_id", activity_info.workflow_run_id)
            try:
                return await super().execute_activity(input)
            except Exception as e:
                if len(input.args) == 1:
                    [arg] = input.args
                    if dataclasses.is_dataclass(arg) and not isinstance(arg, type):
                        sentry_sdk.set_context("temporal.activity.input", dataclasses.asdict(arg))
                sentry_sdk.set_context("temporal.activity.info", activity.info().__dict__)
                sentry_sdk.capture_exception()
                raise e


class _SentryWorkflowInterceptor(temporalio.worker.WorkflowInboundInterceptor):
    async def execute_workflow(self, input: temporalio.worker.ExecuteWorkflowInput) -> typing.Any:
        with sentry_sdk.Hub(sentry_sdk.Hub.current):
            sentry_sdk.set_tag("temporal.execution_type", "workflow")
            sentry_sdk.set_tag("module", input.run_fn.__module__ + "." + input.run_fn.__qualname__)
            workflow_info = workflow.info()
            _set_common_workflow_tags(workflow_info)
            sentry_sdk.set_tag("temporal.workflow.task_queue", workflow_info.task_queue)
            sentry_sdk.set_tag("temporal.workflow.namespace", workflow_info.namespace)
            sentry_sdk.set_tag("temporal.workflow.run_id", workflow_info.run_id)
            try:
                return await super().execute_workflow(input)
            except Exception as e:
                if len(input.args) == 1:
                    [arg] = input.args
                    if dataclasses.is_dataclass(arg) and not isinstance(arg, type):
                        sentry_sdk.set_context("temporal.workflow.input", dataclasses.asdict(arg))
                sentry_sdk.set_context("temporal.workflow.info", workflow.info().__dict__)

                if not workflow.unsafe.is_replaying():
                    with workflow.unsafe.sandbox_unrestricted():
                        sentry_sdk.capture_exception()
                raise e


class SentryInterceptor(temporalio.worker.Interceptor):
    def intercept_activity(
        self, next: temporalio.worker.ActivityInboundInterceptor
    ) -> temporalio.worker.ActivityInboundInterceptor:
        return _SentryActivityInboundInterceptor(super().intercept_activity(next))

    def workflow_interceptor_class(
        self, input: temporalio.worker.WorkflowInterceptorClassInput
    ) -> typing.Optional[typing.Type[temporalio.worker.WorkflowInboundInterceptor]]:
        return _SentryWorkflowInterceptor
