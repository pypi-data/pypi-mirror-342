import concurrent.futures as cf
import asyncio
import inspect
from typing import (
    Awaitable,
    Never,
    Callable,
    Literal,
    Optional,
    ParamSpec,
    TypeVar,
    Union,
    Coroutine,
    overload,
)
from ._func_cache import CacheConf
from ._async_func_decorator import wrap_async
from ._run_sync_in_executor import wrap_sync

R = TypeVar("R")
P = ParamSpec("P")


class FuncDecorator:
    def __init__(
        self,
        cache: Optional[CacheConf | dict] = None,
        executor: Literal["thread", "process"] = "thread",
        with_script_run_context: bool = False,
    ):
        self.__cache = cache
        self.__executor = executor
        self.__with_script_run_context = with_script_run_context

    @overload
    def __call__(
        self,
        func: Union[Callable[P, Awaitable[R]], Callable[P, Coroutine[None, None, R]]],
    ) -> Callable[P, Awaitable[R]]: ...

    @overload
    def __call__(
        self,
        func: Callable[P, R],
    ) -> Callable[P, Awaitable[R]]: ...

    def __call__(self, func):
        assert callable(func), "expected a Callable"
        assert not inspect.isgeneratorfunction(func) and not inspect.isasyncgenfunction(
            func
        ), "expected a non-generator Cunction"
        if inspect.iscoroutinefunction(func):
            return wrap_async(
                cache=self.__cache,
                executor=self.__executor,
                with_script_run_context=self.__with_script_run_context,
            )(func)
        else:
            return wrap_sync(
                cache=self.__cache,
                executor=self.__executor,
                with_script_run_context=self.__with_script_run_context,
            )(func)


def run_in_executor(
    cache: Optional[CacheConf | dict] = None,
    # TODO: support process pool executor (Th)
    # TODO: support custom executor
    executor: Literal["thread", "process"] = "thread",
    with_script_run_context: bool = False,
) -> FuncDecorator:
    return FuncDecorator(
        cache=cache, executor=executor, with_script_run_context=with_script_run_context
    )
