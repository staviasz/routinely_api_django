from typing import get_args
from drf_yasg import openapi

from modules.tasks import TaskCategories, TaskType


class CreateTaskDoc:
    tags = (["task"],)
    operation_description = "Criar uma nova tarefa"
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Nome da tarefa",
                example="Tarefa 1",
            ),
            "description": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Descrição da tarefa",
                example="Descrição da tarefa 1",
            ),
            "category": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=(
                    f"Categoria da tarefa, pode ser: {', '.join(get_args(TaskCategories))}"
                ),
                example="career",
            ),
            "type": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=f"Tipo da tarefa, pode ser: {', '.join(get_args(TaskType))}",
                example="habit",
            ),
            "date_time": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Data de início da tarefa",
                example="2022-01-01 00:00",
            ),
            "weekdays": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
                description="Dias da semana em que a tarefa será executada",
                example=["monday", "tuesday"],
            ),
            "finally_datetime": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Data de conclusão da tarefa",
                example="2022-01-01 00:00",
            ),
        },
        required=["name", "description", "category", "type", "datetime"],
    )
    responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "account_id": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="ID da conta",
                    example="fb0e2f3b-a90e-4f3c-b292-11bbf44a637a",
                ),
            },
        ),
        400: "Erro de validação",
        401: "Token inválido",
        500: "Erro interno do servidor",
    }


class ListTaskDoc:
    tags = (["task"],)
    operation_description = "A listagem será feita com as tasks do mês e ano informados, caso não seja informado, a data atual será usada"
    manual_parameters = [
        openapi.Parameter(
            name="month",
            in_=openapi.IN_QUERY,
            description="Mês da tarefa (1 a 12).",
            type=openapi.TYPE_INTEGER,
            example=1,
        ),
        openapi.Parameter(
            name="year",
            in_=openapi.IN_QUERY,
            description="Ano da tarefa.",
            type=openapi.TYPE_INTEGER,
            example=2022,
        ),
    ]
    responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "account_id": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="ID da conta",
                    example="fb0e2f3b-a90e-4f3c-b292-11bbf44a637a",
                ),
            },
        ),
        400: "Erro de validação",
        401: "Token inválido",
        500: "Erro interno do servidor",
    }


class UpdateTaskDoc:
    tags = (["task"],)
    operation_description = "Atualizar uma tarefa"
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="ID da tarefa",
                example="fb0e2f3b-a90e-4f3c-b292-11bbf44a637a",
            ),
            "name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Nome da tarefa",
                example="Tarefa 1",
            ),
            "description": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Descrição da tarefa",
                example="Descrição da tarefa 1",
            ),
            "category": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=(
                    f"Categoria da tarefa, pode ser: {', '.join(get_args(TaskCategories))}"
                ),
                example="career",
            ),
            "type": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=f"Tipo da tarefa, pode ser: {', '.join(get_args(TaskType))}",
                example="habit",
            ),
            "datetime": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Data de início da tarefa",
                example="2022-01-01 00:00",
            ),
            "finally_datetime": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Data de conclusão da tarefa",
                example="2022-01-01 00:00",
            ),
        },
        required=["id"],
    )
    responses = {
        204: "Tarefa atualizada com sucesso",
        400: "Erro de validação",
        401: "Token inválido",
        500: "Erro interno do servidor",
    }


class DeleteTaskDoc:
    tags = (["task"],)
    operation_description = "Deletar uma tarefa"
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="ID da tarefa",
                example="fb0e2f3b-a90e-4f3c-b292-11bbf44a637a",
            ),
        },
        required=["id"],
    )
    responses = {
        204: "Tarefa deletada com sucesso",
        400: "Erro de validação",
        401: "Token inválido",
        500: "Erro interno do servidor",
    }
