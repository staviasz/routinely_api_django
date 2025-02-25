import json as J
from typing import TypedDict, cast
from django.test import Client


class RequestProps(TypedDict, total=False):
    path: str
    headers: dict
    data: dict | None


class RequestClient:

    def __init__(self):
        self.client = Client()
        self.base_url = "http://127.0.0.1:8000"

    def post(self, props: RequestProps):
        return self.client.post(**self.mapper_request(props))

    def get(self, props: RequestProps):
        new_props = self.mapper_request(props)
        del new_props["data"]
        return self.client.get(**new_props)

    def delete(self, props: RequestProps):
        new_props = self.mapper_request(props)
        del new_props["data"]
        return self.client.delete(**new_props)

    def put(self, props: RequestProps):
        return self.client.put(**self.mapper_request(props))

    def patch(self, props: RequestProps):
        return self.client.patch(**self.mapper_request(props))

    def mapper_request(self, request: RequestProps) -> RequestProps:
        path = f"{self.base_url}{request.get('path', '/')}"
        headers = request.get("headers", {})
        data = J.dumps(request.get("data")) or None
        return cast(
            RequestProps,
            {
                "path": path,
                "headers": headers,
                "data": data,
                "content_type": "application/json",
            },
        )
