import streamlit
from typing import Callable, Generic, Self, Type, TypeVar, Any, Dict
from ._func_util import assert_st_script_run_ctx
import logging

logger = logging.getLogger(__name__)

S = TypeVar("S")


class StateRef(Generic[S]):
    """
    A reference to access a slot in dict-like state storage. The storage is in st.session_state.

    Methods are accessilble from all threads but not thread safe. Caller is expected to coordinate for stronger guarantees.
    """

    def __init__(
        self,
        storage: Dict,
        key: str,
    ):
        self.__storage = storage
        self.__key = key

    def init(self, factory: Callable[[], S]) -> Self:
        if self.__key not in self.__storage:
            self.__storage[self.__key] = factory()
        return self

    @property
    def value(self) -> S:
        return self.__storage[self.__key]

    def set(self, value: S):
        self.__storage[self.__key] = value
        return self

    def reduce(self, compute: Callable[[S], S]) -> S:
        self.__storage[self.__key] = compute(self.value)
        return self.value

    def clear(self):
        if self.__key in self.__storage:
            # orig_value = self.__storage[self.__key]
            del self.__storage[self.__key]
            # return orig_value


def use_state(
    key: str, namespace: str | None = None, type_: Type[S] = Type[Any]
) -> StateRef[S]:
    assert_st_script_run_ctx("use_state()")
    storage = streamlit.session_state.get("_streamlit_concurrency_states")
    if storage is None:
        logger.debug(f"initializing state storage for Streamlit session")
        storage = {}
        streamlit.session_state["_streamlit_concurrency_states"] = storage
    full_key = f"{namespace}:|:{key}"
    return StateRef(storage, full_key)
