from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from django_.adapter.drf_adapter import DRFAdapter
from django_.view.decorators.bearer_token import bearer_token
from modules.tasks.factories import (
    create_task_controller_factory,
    update_task_controller_factory,
    delete_task_controller_factory,
    list_task_controller_factory,
)

from drf_yasg.utils import swagger_auto_schema
from django_.view.docs.task_docs import (
    CreateTaskDoc,
    DeleteTaskDoc,
    ListTaskDoc,
    UpdateTaskDoc,
)


class TaskViews:
    class NoParametersView(APIView):
        @swagger_auto_schema(
            tags=CreateTaskDoc.tags,
            operation_description=CreateTaskDoc.operation_description,
            request_body=CreateTaskDoc.request_body,
            responses=CreateTaskDoc.responses,
        )
        @bearer_token
        def post(self, request: Request) -> Response:
            adapter = DRFAdapter(create_task_controller_factory())
            return adapter.adapt(request)

        @swagger_auto_schema(
            tags=ListTaskDoc.tags,
            operation_description=ListTaskDoc.operation_description,
            manual_parameters=ListTaskDoc.manual_parameters,
            responses=ListTaskDoc.responses,
        )
        @bearer_token
        def get(self, request: Request) -> Response:
            adapter = DRFAdapter(list_task_controller_factory())
            return adapter.adapt(request)

    class WithParametersView(APIView):

        @swagger_auto_schema(
            tags=UpdateTaskDoc.tags,
            operation_description=UpdateTaskDoc.operation_description,
            request_body=UpdateTaskDoc.request_body,
            responses=UpdateTaskDoc.responses,
        )
        @bearer_token
        def put(self, request: Request, id) -> Response:
            adapter = DRFAdapter(update_task_controller_factory())
            return adapter.adapt(request, id=id)

        @swagger_auto_schema(
            tags=DeleteTaskDoc.tags,
            operation_description=DeleteTaskDoc.operation_description,
            request_body=DeleteTaskDoc.request_body,
            responses=DeleteTaskDoc.responses,
        )
        @bearer_token
        def delete(self, request: Request, id) -> Response:
            adapter = DRFAdapter(delete_task_controller_factory())
            return adapter.adapt(request, id=id)
