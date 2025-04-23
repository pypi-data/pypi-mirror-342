import datetime
import typing

import temporalio.common

from gadfastemporal import enums


def once(
    *,
    run_timeout: typing.Optional[datetime.timedelta] = None,
    execution_timeout: typing.Optional[datetime.timedelta] = None,
    retry_maximum_attempts: int = 1,
    retry_initial_interval: datetime.timedelta = datetime.timedelta(seconds=1),
    retry_backoff_coefficient: float = 2.0,
    retry_maximum_interval: typing.Optional[datetime.timedelta] = None,
) -> dict:
    return {
        enums.PolicyAttribute.run_timeout: run_timeout,
        enums.PolicyAttribute.execution_timeout: execution_timeout,
        enums.PolicyAttribute.retry_policy: temporalio.common.RetryPolicy(
            maximum_attempts=retry_maximum_attempts,
            initial_interval=retry_initial_interval,
            backoff_coefficient=retry_backoff_coefficient,
            maximum_interval=retry_maximum_interval,
        ),
    }


__all__ = ["once"]
