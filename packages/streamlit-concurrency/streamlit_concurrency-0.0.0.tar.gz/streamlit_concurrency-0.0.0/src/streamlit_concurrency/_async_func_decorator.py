import asyncio
import concurrent.futures as cf
import streamlit as st
from asgiref.sync import async_to_sync
from concurrent.futures import Executor
import logging

from typing import (
    Awaitable,
    Literal,
    Optional,
    TypeVar,
    Callable,
    ParamSpec,
    overload,
    cast,
)
from ._func_cache import CacheConf
from ._func_util import assert_is_async
from ._executors import get_executor

logger = logging.getLogger(__name__)

R = TypeVar("R")
P = ParamSpec("P")


def wrap_async(
    cache: Optional[CacheConf | dict] = None,
    executor: Executor | Literal["thread", "process"] = "thread",
    with_script_run_context: bool = False,
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    if isinstance(executor, str):
        executor = get_executor(executor)
    if not isinstance(executor, cf.Executor):
        raise ValueError(
            f"executor must be 'thread', 'process' or an instance of concurrent.futures.Executor, got {executor}"
        )
    thread_executor = get_executor("thread")

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        assert_is_async(func)

        async def wrapper(*args, **kwargs) -> R:
            # the sync function to run in the executor
            def dispatched(*args, **kwargs) -> R:
                return async_to_sync()(func)(*args, **kwargs)

            # the sync function that can be cache_data-ed
            def dispatch_and_wait(*args, **kwargs) -> R:
                return executor.submit(dispatched, *args, **kwargs).result()

            if cache is not None:
                # st.cache_data needs the real user function
                # its cache key depends on code position and code text
                real_func = st.cache_data(dispatch_and_wait, **cache)
            else:
                real_func = dispatch_and_wait

            future = thread_executor.submit(real_func, *args, **kwargs)
            return await asyncio.wrap_future(future)

        return wrapper

    return decorator
