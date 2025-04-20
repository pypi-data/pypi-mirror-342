# lpsmods-api

![Tests](https://github.com/legopitstop/lpsmods-api/actions/workflows/tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/lpsmods-api)](https://pypi.org/project/lpsmods-api/)
[![Python](https://img.shields.io/pypi/pyversions/lpsmods-api)](https://www.python.org/downloads//)
![Downloads](https://img.shields.io/pypi/dm/lpsmods-api)
![Status](https://img.shields.io/pypi/status/lpsmods-api)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Issues](https://img.shields.io/github/issues/legopitstop/lpsmods-api)](https://github.com/legopitstop/lpsmods-api/issues)

Python API wrapper for api.lpsmods.dev.

## Installation

Install the module with pip:

```bat
pip3 install lpsmods-api
```

Update existing installation: `pip3 install lpsmods-api --upgrade`

## Requirements

| Name                                             | Usage               |
| ------------------------------------------------ | ------------------- |
| [`requests`](https://pypi.org/project/requests/) | For HTTP requests   |
| [`pydantic`](https://pypi.org/project/pydantic/) | For response models |

## Examples

```Python
from lpsmods_api import LPSModsClient

api = LPSModsClient()
api.fetch_info()
```
