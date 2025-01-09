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
            "body": request.data,
            "query": request.query_params.dict(),
            "params": request.parser_context.get("kwargs", {}),
        }

        response = asyncio.run(self.controller.execute(controller_request))

        return Response(
            data=response["body"],
            status=response["status"],
        )
