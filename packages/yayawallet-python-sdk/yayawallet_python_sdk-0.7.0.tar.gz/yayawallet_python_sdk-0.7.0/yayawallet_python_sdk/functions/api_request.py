import os
import httpx
from yayawallet_python_sdk.functions.get_time import get_time
from typing import Dict, Optional
from django.http import StreamingHttpResponse
from yayawallet_python_sdk.functions.generate_signature import generate_signature
import json

async def api_request(
    method: str,
    path: str,
    params: dict,
    data: Optional[Dict] = None,
    api_key: Optional[str] = None,
):    
    url = os.getenv("YAYA_API_URL", "") + path
    YAYA_API_PATH = os.getenv("YAYA_API_PATH", "") + path

    unix_time_response = await get_time()
    unix_time = str(unix_time_response['time'])
    json_body = ""
    if data is not None:
        json_body = json.dumps(data)
        
    signed_payload, used_api_key = await generate_signature(
        unix_time, method, YAYA_API_PATH, json_body, api_key
    )
        
    headers = {
        "Content-Type": "application/json",
        "YAYA-API-KEY": used_api_key,
        "YAYA-API-TIMESTAMP": unix_time,
        "YAYA-API-SIGN": signed_payload,
    }
        
    try:
        if method == "POST":
            response = await httpx.AsyncClient().post(
                url, params=params, headers=headers, json=data, timeout=100.0
            )
        elif method == "PUT":
            response = await httpx.AsyncClient().put(
                url, headers=headers, params=params, json=data, timeout=100.0
            )
        elif method == "DELETE":
            response = await httpx.AsyncClient().delete(
                url, params=params, headers=headers, timeout=100.0
            )
        else:
            response = await httpx.AsyncClient().get(
                url, params=params, headers=headers, timeout=100.0
            )
            
        return StreamingHttpResponse(
            response.text,
            content_type=response.headers.get('content-type'),
            status=response.status_code,
            reason=response.reason_phrase
        )
    except Exception as e:
        print(f"API request failed: {e}")
        raise