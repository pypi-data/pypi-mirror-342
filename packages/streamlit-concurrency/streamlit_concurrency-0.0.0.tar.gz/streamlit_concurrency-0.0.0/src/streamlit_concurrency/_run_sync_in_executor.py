import streamlit as st
import functools
import concurrent.futures as cf
from typing import (
    Awaitable,
    Literal,
    Optional,
    TypeVar,
    Callable,
    ParamSpec,
)
import asyncio
import contextlib
import logging
from ._func_util import (
    dump_func_metadata,
    assert_is_sync,
    assert_st_script_run_ctx,
    create_script_run_context_cm,
)
from ._func_cache import CacheConf
from ._executors import get_executor

R = TypeVar("R")
P = ParamSpec("P")

logger = logging.getLogger(__name__)


# @overload
# def wrap_sync(
#     cache: Optional[CacheConf | dict] = None,
#     executor: Executor | Literal["thread_pool", "process_pool"] = "thread_pool",
#     with_script_run_context: bool = False,
#     async_=True,
# ) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]: ...


def wrap_sync(
    cache: Optional[CacheConf | dict] = None,
    executor: cf.Executor | Literal["thread", "process"] = "thread",
    with_script_run_context: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, Awaitable[R]]]:
    """Transforms a sync function to run in executor and return result as Awaitable

    @param cache: configuration to pass to st.cache_data()

    @param executor: executor to run the function in, can be 'thread_pool', 'process_pool' or an concurrent.futures.Executor

    @param with_script_run_context: if True, the function will be run with a ScriptRunContext. Must be used with a ThreadPoolExecutor.

    See [multithreading](https://docs.streamlit.io/develop/concepts/design/multithreading) for possible motivation and consequences.

    """
    if isinstance(executor, str):
        executor = get_executor(executor)
    if not isinstance(executor, cf.Executor):
        raise ValueError(
            f"executor must be 'thread', 'process' or an instance of concurrent.futures.Executor, got {executor}"
        )

    if with_script_run_context and not isinstance(executor, cf.ThreadPoolExecutor):
        raise ValueError(
            "with_script_run_context=True can only be used with a ThreadPoolExecutor"
        )

    def decorator(func: Callable):
        assert_is_sync(func)

        dump_func_metadata(func)

        def wrapper(*args, **kwargs):
            # a wrapper that
            # 1. capture possible ScriptRunContext
            # 2. run decorated `func` in executor, with a context-managed ScriptRunContext
            # 3. return a Awaitable
            if with_script_run_context:
                cm = create_script_run_context_cm(assert_st_script_run_ctx())
            else:
                cm = contextlib.nullcontext()

            def func_for_executor():
                # NOTE: need to make sure this works with other executors
                with cm:
                    if cache is not None:
                        # st.cache_data needs the real user function
                        # its cache key depends on code position and code text
                        real_func = st.cache_data(func, **cache)
                    else:
                        real_func = func

                    return real_func(*args, **kwargs)

            future = executor.submit(func_for_executor)
            return asyncio.wrap_future(future)

        return functools.update_wrapper(wrapper, func)

    return decorator
