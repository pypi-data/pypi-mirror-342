import typing

from temporalio import workflow


class Workflow:
    @staticmethod
    def id(*args, **kwargs) -> str:
        raise NotImplementedError

    @staticmethod
    def activities() -> typing.List[typing.Callable]:
        raise NotImplementedError

    @workflow.run
    async def run(self, command: typing.Any) -> typing.Any:
        raise NotImplementedError
