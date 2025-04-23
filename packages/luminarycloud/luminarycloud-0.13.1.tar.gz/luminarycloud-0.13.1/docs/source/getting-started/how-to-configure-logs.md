# Configure Logs

The Luminary Cloud Python SDK uses [Python's built-in logging module](https://docs.python.org/3/library/logging.html). By default, Python's root logger has a log-level of WARNING and writes to stdout. For more details, including how to use configuration files and/or set up
different handlers, refer to [Python's official documentation](https://docs.python.org/3/library/logging.config.html).

Specific examples for configuring SDK logs can be found below.

:::{tip}
We recommend all users follow the instructions below to configure a log file
location. This log file can help us better support you with SDK issues.
:::

## Configuration

The following example demonstrates how to configure the SDK logger to write
debug-level logs to `logs.txt`.

Your own logs will not be affected if using this configuration (unless you have
a logger whose name starts with `luminarycloud`).

```python3
import logging

logger = logging.getLogger('luminarycloud')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler("logs.txt"))
```
