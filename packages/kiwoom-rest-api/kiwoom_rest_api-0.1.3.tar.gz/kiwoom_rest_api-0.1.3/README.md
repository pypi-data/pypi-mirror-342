# Kiwoom REST API

Python client for interacting with Kiwoom Securities REST API.

## Installation

```bash
pip install kiwoom-rest-api
```

## Usage

```python
    import os
    os.environ["KIWOOM_API_KEY"] = "your_api_key"
    os.environ["KIWOOM_API_SECRET"] = "your_api_secret"

    from kiwoom_rest_api.koreanstock.stockinfo import StockInfo
    from kiwoom_rest_api.auth.token import TokenManager

    # 토큰 매니저 초기화
    token_manager = TokenManager()
    print(f"\n\n★@token_manager: {token_manager}\n\n")
    # StockInfo 인스턴스 생성 (base_url 수정)
    stock_info = StockInfo(base_url="https://api.kiwoom.com", token_manager=token_manager)

    try:
        result = stock_info.basic_stock_information_request_ka10001("005930")
        print("API 응답:", result)
    except Exception as e:
        print("에러 발생:", str(e))
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
[pypi-keys]()



# License

This project is licensed under the terms of the MIT license.