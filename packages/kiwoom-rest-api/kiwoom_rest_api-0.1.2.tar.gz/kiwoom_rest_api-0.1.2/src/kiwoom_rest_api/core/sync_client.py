from typing import Any, Dict, Optional

import httpx

from kiwoom_rest_api.core.base import prepare_request_params, process_response

def make_request(
    endpoint: str,
    method: str = "GET",
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, Any]] = None,
    access_token: Optional[str] = None,
    timeout: Optional[float] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    
    print(f"\n\n@endpoint: {endpoint}")
    print(f"\n\n@method: {method}")
    print(f"\n\n@params: {params}")
    print(f"\n\n@data: {data}")
    print(f"\n\n@headers: {headers}")
    print(f"\n\n@access_token: {access_token}")
    print(f"\n\n@timeout: {timeout}")
    """Make a synchronous HTTP request to the Kiwoom API"""
    request_params = prepare_request_params(
        endpoint=endpoint,
        method=method,
        params=params,
        data=data,
        headers=headers,
        access_token=access_token,
        timeout=timeout,
    )
    
    # 추가: kwargs에서 json 데이터 처리
    if 'json' in kwargs and method in ["POST", "PUT", "PATCH"]:
        request_params["json"] = kwargs['json']
    
    print(f"\n\n@@request_params.get(params): {request_params.get('params')}")
    print(f"\n\n@@request_params.get(json): {request_params.get('json')}")
    print(f"\n\n@@request_params: {request_params}\n\n")
    
    # data = {
    #     "grant_type": "client_credentials",
    #     "appkey": request_params["headers"]["appkey"],
    #     "secretkey": request_params["headers"]["appsecret"],
    # }
    
    # request_params["method"] = "POST"
    # request_params["url"] = "https://api.kiwoom.com/oauth2/token"
    # request_params["json"] = data
    # request_params["headers"] = {"Content-Type": "application/json;charset=UTF-8"}
    # request_params["timeout"] = 10.0
    
    print(f"\n\n@request_params.get(params): {request_params.get('params')}")
    print(f"\n\n@request_params.get(json): {request_params.get('json')}")
    print(f"\n\n@request_params[url]: {request_params['url']}\n\n")
    with httpx.Client() as client:
        response = client.request(
            method=request_params["method"],
            url=request_params["url"],
            params=request_params.get("params"),
            json=request_params.get("json"),
            headers=request_params["headers"],
            timeout=request_params["timeout"],
        )
        
        print(f"\n\n@response: {response}")
        
        return process_response(response)
