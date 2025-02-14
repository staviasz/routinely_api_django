from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from django_.adapter.drf_adapter import DRFAdapter
from django_.view.decorators.bearer_token import bearer_token
from django_.view.docs.customer_docs import (
    RegisterCustomerDoc,
    LoginCustomerDoc,
    ConfirmCodeToResetPasswordCustomerDoc,
    ForgetPasswordDoc,
    NewPasswordDoc,
    RefreshLoginDoc,
    ConfirmEmailDoc,
)
from modules.customer.factories import (
    register_customer_controller_factory,
    login_controller_factory,
    confirm_code_to_reset_password_controller_factory,
    forget_password_controller_factory,
    new_password_controller_factory,
    refresh_login_controller_factory,
    confirm_email_controller_factory,
)


class RegisterCustomerView(APIView):
    @swagger_auto_schema(
        tags=RegisterCustomerDoc.tags,
        operation_description=RegisterCustomerDoc.operation_description,
        request_body=RegisterCustomerDoc.request_body,
        responses=RegisterCustomerDoc.responses,
        manual_parameters=RegisterCustomerDoc.manual_parameters,
        security=RegisterCustomerDoc.security,
    )
    def post(self, request: Request) -> Response:
        adapter = DRFAdapter(register_customer_controller_factory())

        return adapter.adapt(request)


class LoginCustomerView(APIView):
    @swagger_auto_schema(
        tags=LoginCustomerDoc.tags,
        operation_description=LoginCustomerDoc.operation_description,
        request_body=LoginCustomerDoc.request_body,
        responses=LoginCustomerDoc.responses,
        security=LoginCustomerDoc.security,
    )
    def post(self, request: Request) -> Response:
        adapter = DRFAdapter(login_controller_factory())

        return adapter.adapt(request)


class ConfirmCodeToResetPasswordView(APIView):
    @swagger_auto_schema(
        tags=ConfirmCodeToResetPasswordCustomerDoc.tags,
        operation_description=ConfirmCodeToResetPasswordCustomerDoc.operation_description,
        request_body=ConfirmCodeToResetPasswordCustomerDoc.request_body,
        responses=ConfirmCodeToResetPasswordCustomerDoc.responses,
        security=ConfirmCodeToResetPasswordCustomerDoc.security,
    )
    def post(self, request: Request) -> Response:
        adapter = DRFAdapter(confirm_code_to_reset_password_controller_factory())

        return adapter.adapt(request)


class ForgetPasswordView(APIView):
    @swagger_auto_schema(
        tags=ForgetPasswordDoc.tags,
        operation_description=ForgetPasswordDoc.operation_description,
        request_body=ForgetPasswordDoc.request_body,
        responses=ForgetPasswordDoc.responses,
        security=ForgetPasswordDoc.security,
    )
    def post(self, request: Request) -> Response:
        adapter = DRFAdapter(forget_password_controller_factory())

        return adapter.adapt(request)


class NewPasswordView(APIView):
    @swagger_auto_schema(
        tags=NewPasswordDoc.tags,
        operation_description=NewPasswordDoc.operation_description,
        request_body=NewPasswordDoc.request_body,
        responses=NewPasswordDoc.responses,
        security=NewPasswordDoc.security,
    )
    def post(self, request: Request) -> Response:
        adapter = DRFAdapter(new_password_controller_factory())

        return adapter.adapt(request)


class RefreshLoginView(APIView):
    @swagger_auto_schema(
        tags=RefreshLoginDoc.tags,
        operation_description=RefreshLoginDoc.operation_description,
        request_body=RefreshLoginDoc.request_body,
        responses=RefreshLoginDoc.responses,
        security=RefreshLoginDoc.security,
    )
    def post(self, request: Request) -> Response:
        adapter = DRFAdapter(refresh_login_controller_factory())
        print("esta passando mesmo sem o token")

        return adapter.adapt(request)


class ConfirmEmailView(APIView):
    @swagger_auto_schema(
        tags=ConfirmEmailDoc.tags,
        operation_description=ConfirmEmailDoc.operation_description,
        responses=ConfirmEmailDoc.responses,
        manual_parameters=ConfirmEmailDoc.manual_parameters,
        security=ConfirmEmailDoc.security,
    )
    def get(self, request: Request) -> Response:
        adapter = DRFAdapter(confirm_email_controller_factory())

        return adapter.adapt(request)
