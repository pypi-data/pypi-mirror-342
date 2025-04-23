import typing

import temporalio.workflow

from gadfastemporal import policies


class Executor:
    def __init__(self, task_queue: str) -> None:
        self._task_queue = task_queue

    async def sync(
        self,
        handler: typing.Callable[..., typing.Any],
        *args: typing.Any,
        policy: dict | None = None,
    ) -> typing.Any:
        return await temporalio.workflow.execute_activity_method(
            activity=handler,
            args=list(args),
            task_queue=self._task_queue,
            cancellation_type=temporalio.workflow.ActivityCancellationType.TRY_CANCEL,
            **policy if policy else policies.activities.sync(),
        )

    async def polling(
        self,
        handler: typing.Callable[..., typing.Any],
        *args: typing.Any,
        policy: dict | None = None,
    ) -> temporalio.workflow.ActivityHandle[typing.Any]:
        return await temporalio.workflow.start_activity_method(
            activity=handler,
            args=list(args),
            task_queue=self._task_queue,
            cancellation_type=temporalio.workflow.ActivityCancellationType.TRY_CANCEL,
            **policy if policy else policies.activities.polling(),
        )


__all__ = ["Executor"]
