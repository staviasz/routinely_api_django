from main.app import HttpResponse
from main.errors import CustomError


def ok(data: dict) -> HttpResponse:
    return {"status": 200, "body": data}


def create(data: dict) -> HttpResponse:
    return {"status": 201, "body": data}


def no_content() -> HttpResponse:
    return {"status": 204, "body": None}


def bad_request(error: CustomError) -> HttpResponse:
    return {"status": 400, "body": {"message": error.formate_errors["messages_error"]}}


def unauthorized(error: CustomError) -> HttpResponse:
    return {"status": 401, "body": {"message": error.formate_errors["messages_error"]}}


def forbidden(error: CustomError) -> HttpResponse:
    return {"status": 403, "body": {"message": error.formate_errors["messages_error"]}}


def not_found(error: CustomError) -> HttpResponse:
    return {"status": 404, "body": {"message": error.formate_errors["messages_error"]}}


def conflict(error: CustomError) -> HttpResponse:
    return {"status": 409, "body": {"message": error.formate_errors["messages_error"]}}


def internal_server_error() -> HttpResponse:
    return {"status": 500, "body": {"message": ["Internal Server Error"]}}
