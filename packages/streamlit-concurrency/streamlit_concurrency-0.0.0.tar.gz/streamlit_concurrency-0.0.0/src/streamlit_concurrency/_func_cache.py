from datetime import timedelta
from streamlit.runtime.caching.cache_data_api import (
    CachePersistType,
)
from streamlit.runtime.caching.hashing import HashFuncsDict
from typing import TypedDict


class CacheConf(TypedDict):
    """params for streamlit.cache_data"""

    ttl: float | timedelta | str | None
    max_entries: int | None
    # show_spinner: bool | str # TODO: see if we can / should support this
    persist: CachePersistType | bool | None
    hash_funcs: HashFuncsDict | None
