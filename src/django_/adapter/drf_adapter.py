import asyncio
from rest_framework.request import Request
from rest_framework.response import Response
from main import BaseController, HttpRequest


class DRFAdapter:
    def __init__(self, controller: BaseController) -> None:
        self.controller = controller

    def adapt(self, request: Request, **kwargs) -> Response:
        controller_request: HttpRequest = {
            "headers": dict(request.headers),
            "body": self.__normalize_body(dict(request.data)),
            "query": self.__normalize_query(dict(request.GET)),
            "params": request.parser_context.get("kwargs", {}),
        }

        print("antes do controller")
        response = asyncio.run(self.controller.execute(controller_request))
        print("depois do controller")

        return Response(
            status=response["status"],
            data=response.get("body"),
            headers=response.get("headers"),
        )

    def __normalize_body(self, body: dict):
        if body is None:
            return None

        format_dict = {}
        for key, value in body.items():
            print(key, value)
            format_dict[key] = value[0] if isinstance(value, list) else value
            print(format_dict)
        return format_dict

    def __normalize_query(self, query: dict):
        if query is None:
            return None

        format_dict = {}
        for index, (key, value) in enumerate(query.items()):
            if (
                len(value) == 1
                and value[0] is None
                or value[0] == "None"
                or value[0].strip() == ""
            ):
                format_dict[str(index)] = key
            else:
                format_dict[key] = value[0]

        return format_dict
