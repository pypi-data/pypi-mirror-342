<div align="center">

# Starlette RAS-handler

[![Supported Python versions](https://img.shields.io/pypi/pyversions/starlette-ras-handle.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/starlette-ras-handle)
[![PyPI version](https://img.shields.io/pypi/v/starlette-ras-handle.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/starlette-ras-handle)
[![PyPI downloads](https://img.shields.io/pypi/dm/starlette-ras-handle.svg)](https://pypi.org/project/starlette-ras-handle)

</div>

This library adds the ability to handle `RuntimeError: Caught handled exception, but response already started.` error, so you can silent it, or do whatever you want

## Installation 📥

```shell
python -m pip install -U starlette-ras-handle 
```


## Usage 🛠️
1. Define an async function that accepts `(Exception, Request | WebSocket)` and returns `None`
    ```python
    async def print_handler(exc: Exception, request: Request | WebSocket) -> None:
        print("Caught", exc)
    ```

2. Patch!
    ```python
    from handler import print_handler
    
    from starlette_ras_handle import handle_starlette_ras
    handle_starlette_ras(print_handler)
    
    # other imports...
    ```
   
**IMPORTANT:** If you want the patch to work properly, you should use it before you import anything, related to `starlette` (e.g. `FastAPI`)

You can check an example in `/examples/example.py`

## Troubleshooting 🚨

If you encounter issues or have queries, feel free to check our [Issues section](https://github.com/barabum0/starlette-ras-handle/issues) on GitHub.

## Contribution 🤝

Contributions are welcome. Please fork the repository, make your changes, and submit a pull request.
