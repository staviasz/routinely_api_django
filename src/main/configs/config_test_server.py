from typing import TypedDict
from django.test import TestCase
from django.test import Client


class RequestProps(TypedDict):
    path: str
    headers: dict
    data: dict


class RequestClient:

    def __init__(self):
        self.client = Client()
        self.base_url = "http://127.0.0.1:8000"

    def post(self, props: RequestProps):
        return self.client.post(**self.mapper_request(props))

    def get(self, props: RequestProps):
        return self.client.get(**self.mapper_request(props))

    def delete(self, props: RequestProps):
        return self.client.delete(**self.mapper_request(props))

    def put(self, props: RequestProps):
        return self.client.put(**self.mapper_request(props))

    def patch(self, props: RequestProps):
        return self.client.patch(**self.mapper_request(props))

    def mapper_request(self, request: RequestProps) -> RequestProps:
        path = f"{self.base_url}{request.get('path', '/')}"
        headers = request.get("headers", {})
        data = request.get("data", {})
        return {"path": path, "headers": headers, "data": data}
