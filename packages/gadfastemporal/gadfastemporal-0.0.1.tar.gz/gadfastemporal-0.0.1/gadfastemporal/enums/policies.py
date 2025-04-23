import enum


class PolicyAttribute(str, enum.Enum):
    start_to_close_timeout = "start_to_close_timeout"
    schedule_to_close_timeout = "schedule_to_close_timeout"
    schedule_to_start_timeout = "schedule_to_start_timeout"
    heartbeat_timeout = "heartbeat_timeout"
    run_timeout = "run_timeout"
    execution_timeout = "execution_timeout"
    retry_policy = "retry_policy"
