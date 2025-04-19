<div align="center">
  <img src="github/logo/pywrapture.png" alt="logo" vspace="5" hspace="5">
  <h1>PYWRAPTURE</h1>
</div>

Python utilities and decorators to simplify your code — elegant, readable, and pythonic.

`pywrapture` is a lightweight module that provides decorators and utility functions for streamlining common Python patterns. It helps make your code cleaner, more readable, and easier to maintain.
This module is particularly useful in production pipelines, testing environments, CLI tooling,
API layers, and any scenario where function behavior needs to be modified, extended,
monitored, or controlled without changing the original function logic.

## Features

- `@retry`         Automatically retry failed functions a configurable number of times.
- `@delay`         Postpone function execution by a given number of seconds.
- `@timer`         Measure and report function execution time.
- `@handle`        Catch and log exceptions to a plain-text file.
- `@JSONhandle`    Log exception details (with context) into a structured JSON file.

- Runtime Flags  Many decorators expose runtime parameters for greater control (e.g., toggle debug).
- Utility functions for common patterns
- Lightweight, no external dependencies
- Python 3.7+

## Installation

```bash
pip install pywrapture
```

Or install from source:

```bash
git clone https://github.com/yourusername/pywrapture.git
cd pywrapture
pip install .
```

## Usage

```python
from pywrapture import safe, retry, timed

@retry(attempts=3, delay=1)
def flaky_function():
    # Example: network call
    ...

@delay(seconds=2)
def slow_function():
    import time
    time.sleep(2)
    return "Done"
```

## License

GPL-3.0 License © 2025 Tkemza
