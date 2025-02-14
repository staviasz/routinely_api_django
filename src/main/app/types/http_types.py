from typing import Any, Dict, Optional, TypedDict


class HttpRequest(TypedDict, total=False):
    params: Optional[Dict[str, Any]]
    query: Optional[Dict[str, Any]]
    headers: Optional[Dict[str, Any]]
    body: Optional[Dict[str, Any]]


class HttpResponse(TypedDict, total=False):
    status: int
    body: Optional[Dict[str, Any]]
    headers: Optional[Dict[str, Any]]
