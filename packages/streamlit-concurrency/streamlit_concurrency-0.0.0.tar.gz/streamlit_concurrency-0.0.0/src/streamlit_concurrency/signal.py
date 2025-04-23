import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx


class PageRunSignal:
    def __init__(self):
        ctx = get_script_run_ctx()
        if ctx is None:
            raise RuntimeError("This function must be called in a Streamlit script.")
        self.__running = True

    @property
    def running(self) -> bool:
        return self.__running


def use_page_signal() -> PageRunSignal:
    s = PageRunSignal()
    return s


class SessionSignal:
    def __init__(self):
        ctx = get_script_run_ctx()
        if ctx is None:
            raise RuntimeError("This function must be called in a Streamlit script.")
        self.__running = True

    @property
    def running(self) -> bool:
        return self.__running


def use_session_signal() -> SessionSignal:
    s = SessionSignal()
    return s
