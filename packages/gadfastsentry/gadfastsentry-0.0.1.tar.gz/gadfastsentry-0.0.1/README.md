<p align="center">
  <a href="https://github.com/AlexDemure/gadfastsentry">
    <a href="https://ibb.co/hJvgPB9K"><img src="https://i.ibb.co/0R3ngC2f/logo.png" alt="logo" border="0"></a>
  </a>
</p>

<p align="center">
  A production-ready sentry configuration module for Python.
</p>

---

### Installation

```
pip install gadfastsentry
```

### Usage

```python
import logging

import sentry_sdk
from fastapi import FastAPI
from fastapi import Request
from gadfastsentry import Sentry

Sentry(dsn="***", env="production")

app = FastAPI()


@app.middleware("http")
async def inject_trace(request: Request, call_next):
    sentry_sdk.set_extra("trace_id", "12345")
    return await call_next(request)


@app.get("/sentry-debug")
async def trigger_error():
    try:
        division_by_zero = 1 / 0
    except Exception as e:
        logging.error(str(e), exc_info=True)
```
