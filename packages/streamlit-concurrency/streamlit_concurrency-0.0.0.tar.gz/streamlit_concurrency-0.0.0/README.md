# streamlit-concurrency

Easier and safer concurrency for streamlit.

This library provides helpers to

- run slow code in ThreadPoolExecutor and gather result in script thread
- simply call Streamlit API from other thread
- manage page state in and across pages
- and more

## `run_in_executor`: transform sync or async function to run in executor

```py
# TODO
```

## `use_state`: page- or session- scoped state

TODO: demo


## How it works

See [how threads work in streamlit](https://docs.streamlit.io/develop/concepts/design/multithreading).

## License

MIT