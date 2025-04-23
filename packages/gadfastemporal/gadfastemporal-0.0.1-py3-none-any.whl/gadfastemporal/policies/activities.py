import datetime
import typing

import temporalio.common

from gadfastemporal import enums


def sync(
    *,
    start_to_close_timeout: datetime.timedelta = datetime.timedelta(hours=1),
    schedule_to_close_timeout: typing.Optional[datetime.timedelta] = None,
    schedule_to_start_timeout: typing.Optional[datetime.timedelta] = None,
    heartbeat_timeout: typing.Optional[datetime.timedelta] = None,
    retry_maximum_attempts: int = 3,
    retry_initial_interval: datetime.timedelta = datetime.timedelta(seconds=1),
    retry_backoff_coefficient: float = 2.0,
    retry_maximum_interval: typing.Optional[datetime.timedelta] = None,
) -> dict:
    return {
        enums.PolicyAttribute.start_to_close_timeout: start_to_close_timeout,
        enums.PolicyAttribute.schedule_to_close_timeout: schedule_to_close_timeout,
        enums.PolicyAttribute.schedule_to_start_timeout: schedule_to_start_timeout,
        enums.PolicyAttribute.heartbeat_timeout: heartbeat_timeout,
        enums.PolicyAttribute.retry_policy: temporalio.common.RetryPolicy(
            maximum_attempts=retry_maximum_attempts,
            initial_interval=retry_initial_interval,
            backoff_coefficient=retry_backoff_coefficient,
            maximum_interval=retry_maximum_interval,
        ),
    }


def polling(
    *,
    start_to_close_timeout: datetime.timedelta = datetime.timedelta(hours=1),
    schedule_to_close_timeout: typing.Optional[datetime.timedelta] = None,
    schedule_to_start_timeout: typing.Optional[datetime.timedelta] = None,
    heartbeat_timeout: datetime.timedelta = datetime.timedelta(minutes=1),
    retry_maximum_attempts: int = 3,
    retry_initial_interval: datetime.timedelta = datetime.timedelta(seconds=1),
    retry_backoff_coefficient: float = 2.0,
    retry_maximum_interval: typing.Optional[datetime.timedelta] = None,
) -> dict:
    return {
        enums.PolicyAttribute.start_to_close_timeout: start_to_close_timeout,
        enums.PolicyAttribute.schedule_to_close_timeout: schedule_to_close_timeout,
        enums.PolicyAttribute.schedule_to_start_timeout: schedule_to_start_timeout,
        enums.PolicyAttribute.heartbeat_timeout: heartbeat_timeout,
        enums.PolicyAttribute.retry_policy: temporalio.common.RetryPolicy(
            maximum_attempts=retry_maximum_attempts,
            initial_interval=retry_initial_interval,
            backoff_coefficient=retry_backoff_coefficient,
            maximum_interval=retry_maximum_interval,
        ),
    }


__all__ = ["sync", "polling"]
