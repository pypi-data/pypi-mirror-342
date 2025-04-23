import inspect
import contextlib
import threading
import logging
from typing import Callable
import sys
import os


from streamlit.runtime.scriptrunner import (
    get_script_run_ctx,
    add_script_run_ctx,
    ScriptRunContext,
)
from streamlit.runtime.scriptrunner_utils.script_run_context import (
    SCRIPT_RUN_CONTEXT_ATTR_NAME,
)

logger = logging.getLogger(__name__)


def assert_st_script_run_ctx(target="This function") -> ScriptRunContext:
    """Assert that the current thread is the script thread."""
    ctx = get_script_run_ctx(suppress_warning=True)
    if ctx is None:
        raise RuntimeError(
            f"{target} must be called in a thread with ScriptRunContext. Typically a ScriptThread running page code."
        )
    return ctx


def assert_is_async(func):
    """Asserts that the given function is an async function."""
    if not (callable(func) and inspect.iscoroutinefunction(func)):
        raise TypeError(f"Expected an async function, got {func}")
    return func


def assert_is_sync(func):
    """Asserts that the given function is an async function."""
    if not (callable(func) and not inspect.iscoroutinefunction(func)):
        raise TypeError(f"Expected an sync function, got {func}")
    return func


@contextlib.contextmanager
def create_script_run_context_cm(script_run_ctx: ScriptRunContext):
    """Create a context manager that

    - when entering, adds given script_run_ctx to the current thread
    - when exiting, un-adds it from current thread
    """
    existing_ctx = get_script_run_ctx(suppress_warning=True)

    if existing_ctx is not None and existing_ctx is not script_run_ctx:
        raise RuntimeError(
            f"Current thread {threading.current_thread().name} had an unexpected ScriptRunContext: {existing_ctx}."
        )

    add_script_run_ctx(thread=threading.current_thread(), ctx=script_run_ctx)
    yield

    # restore the original context, whether it was None or not (this can't be done with add_script_run_ctx)
    setattr(threading.current_thread(), SCRIPT_RUN_CONTEXT_ATTR_NAME, existing_ctx)
    assert get_script_run_ctx(suppress_warning=True) is existing_ctx


def dump_func_metadata(func: Callable):
    logger.warning(
        "function metadata: %s %s %s %s",
        func.__module__,
        func.__name__,
        func.__qualname__,
        func.__code__,
    )
    logger.warning(
        "getsource: %s",
        inspect.getsource(func),
    )


def log_with_callsite(msg: str, *args, **kwargs):
    logger.warning(
        "pid=%s tid=%s thread=%s %s",
        os.getpid(),
        threading.current_thread().ident,
        threading.current_thread().name,
        msg.format(*args, **kwargs),
    )
