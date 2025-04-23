import typing

from temporalio import workflow as _workflow

from gadfastemporal import typings


def workflow(cls: typings.Class) -> typings.Class:
    return typing.cast(typings.Class, _workflow.defn(cls))


def run(func: typings.Func) -> typings.Func:
    return typing.cast(typings.Func, _workflow.run(func))
