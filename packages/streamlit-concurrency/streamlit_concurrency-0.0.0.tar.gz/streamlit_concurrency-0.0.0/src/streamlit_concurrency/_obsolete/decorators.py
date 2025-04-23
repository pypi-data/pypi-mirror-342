import sys

from typing import Callable, Optional, TypedDict, Union
from concurrent.futures import Executor
# from typing_extensions import Unpack

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


class Param(TypedDict):
    executor: Optional[Union[str, Executor]]
    cache_session: Optional[bool]
    cache_global: Optional[bool]
    cache_size: Optional[int]


class CacheLocation(StrEnum):
    session = "session"  # wrapped function must be called in a thread (either a Script Thread) , or an other
    # GLOBAL = "global"
    executor = "executor"
    CUSTOM = "cache_key"


class ExecutorType(StrEnum):
    threaded = "threaded"
    process = "process"


class DecoratorParams(TypedDict):
    copy_script_run_context: Optional[bool]
    executor: Optional[Union[Executor, ExecutorType]]
    cache_location: Optional[Union[CacheLocation, Callable]]
    cache_size: Optional[int]


class CachedCallable:
    def __init__(self, get_cache_storage: Callable, f: Callable):
        self.get_cache_storage = get_cache_storage
        self.f = f

    def __call__(self, *args, **kwargs):
        cache_storage = self.get_cache_storage()
        return self.f(*args, **kwargs)


def wrap_callable(callable, params: DecoratorParams) -> Callable:
    executor = params.get("executor")
    match executor:
        case ExecutorType.threaded | None:
            from .._executors import sfc_thread_pool_executor

            executor = sfc_thread_pool_executor
        case _ if isinstance(executor, Executor):
            pass
        # case _ if callable(executor):
        # executor = executor()
        case _:
            raise ValueError(f"unrecognized executor: {executor}")
    assert isinstance(executor, Executor), (
        f"executor must be an instance of concurrent.futures.Executor, got {executor}"
    )

    # TODO
    copy_script_run_context = params.get("copy_script_run_context", False)
    if copy_script_run_context:
        raise NotImplementedError("copy_script_run_context is not implemented yet")

    cache_location = params.get("cache_location", None)

    def get_cache_storage() -> dict:
        pass

    def wrapped(*args, **kwargs):
        # TODO
        return callable(*args, **kwargs)

    return wrapped


def run_in_executor(
    copy_script_run_context: Optional[bool] = False,
    executor: Optional[Union[Executor, ExecutorType]] = None,
    cache_location: Optional[Union[CacheLocation, Callable]] = None,
    cache_size: Optional[int] = None,
) -> Callable:
    # too bad we cannot name it 🍛
    def curried(f: Callable):
        assert callable(f), "callable expected. e.g. run_in_executor()(f)"
        return wrap_callable(
            f,
            dict(
                copy_script_run_context=copy_script_run_context,
                executor=executor,
                cache_location=cache_location,
                cache_size=cache_size,
            ),
        )

    return curried
