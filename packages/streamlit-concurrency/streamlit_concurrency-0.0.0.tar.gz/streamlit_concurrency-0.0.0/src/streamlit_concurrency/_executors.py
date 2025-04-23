import functools
import concurrent.futures as cf
from typing import Literal

# TODO this should be lazy inited
# TODO initialization should be mutex-protected


@functools.lru_cache(maxsize=1)
def _get_thread_pool_executor() -> cf.Executor:
    return cf.ThreadPoolExecutor(thread_name_prefix="streamlit-concurrency-")


@functools.lru_cache(maxsize=1)
def _get_process_pool_executor() -> cf.Executor:
    return cf.ProcessPoolExecutor()


@functools.lru_cache(maxsize=1)
def _get_interpreter_pool_executor() -> cf.Executor:
    # should be available since py3.14
    return cf.InterpreterPoolExecutor()


@functools.lru_cache(maxsize=1)
def _get_multiprocess_executor() -> cf.Executor:
    raise NotImplementedError(
        "Multiprocess executor is not implemented yet. Please use thread or process executor instead."
    )


def get_executor(
    executor_type: Literal["thread", "process", "interpreter"],
) -> cf.Executor:
    """Get the executor based on the type."""
    if executor_type == "thread":
        return _get_thread_pool_executor()
    elif executor_type == "process":
        return _get_process_pool_executor()
    elif executor_type == "interpreter":
        return _get_interpreter_pool_executor()
    else:
        raise ValueError(f"Unknown executor type: {executor_type}")
