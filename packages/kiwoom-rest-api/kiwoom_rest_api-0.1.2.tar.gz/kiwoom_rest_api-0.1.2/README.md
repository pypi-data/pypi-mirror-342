# Kiwoom REST API

Python client for interacting with Kiwoom Securities REST API.

## Installation

```bash
pip install kiwoom-rest-api
```

## Usage

```python
from kiwoom_rest_api.api import KiwoomAPI

api = KiwoomAPI()
result = api.get_basic_stock_info("005930")
print(result)
```

## CLI Usage

```bash
kiwoom --help
```











# deploy

## prodution
```
    pip install kiwoom-rest-api
    uv add kiwoom-rest-api
```

### deploy to pypi [site](https://pypi.org/project/kiwoom-rest-api/)
```
    poetry shell
    poetry publish --build
```


## test
```
    pip install -i https://test.pypi.org/simple/ kiwoom-rest-api
```
```
    uv add -i https://test.pypi.org/simple/ kiwoom-rest-api
```

### deploy to test-pypi [site](https://test.pypi.org/project/kiwoom-rest-api/)
```
    poetry shell
    poetry publish --build -r test-pypi
```


# docs
[pypi-keys](https://www.notion.so/pypi-tokens-1d28c2bbc2e080849417f0939de3ffd9)



# License

This project is licensed under the terms of the MIT license.