from typing import Any, Dict, Optional, TypedDict


class HttpRequest(TypedDict):
    params: Optional[Dict[str, Any]]
    query: Optional[Dict[str, Any]]
    headers: Optional[Dict[str, Any]]
    body: Optional[Dict[str, Any]]


class HttpResponse(TypedDict):
    status: int
    body: Optional[Dict[str, Any]]
