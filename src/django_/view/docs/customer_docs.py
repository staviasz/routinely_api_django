from drf_yasg import openapi


class RegisterCustomerDoc:
    tags = (["customer"],)
    operation_description = "Registrar um novo cliente"
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Nome do cliente",
                example="John Doe",
            ),
            "email": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Email do cliente",
                example="john@doe.com",
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=(
                    "Senha do cliente deve ter 6 ou mais caracteres, uma letra "
                    "maiúscula, uma letra minúscula, um número e um caractere especial"
                ),
                example="@Test123",
            ),
            "confirmed_password": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Confirmação de senha do cliente",
                example="@Test123",
            ),
            "accepted_terms": openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description="Aceita os termos e condições",
                example=True,
            ),
        },
        required=["name", "email", "password", "confirmed_password", "accepted_terms"],
    )
    responses = {
        204: "Sucesso",
        400: "Erro de validação",
        409: "Email já cadastrado",
        500: "Erro interno do servidor",
    }


class LoginCustomerDoc:
    tags = (["customer"],)
    operation_description = "Autenticação de cliente"
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Email do cliente",
                example="john@doe.com",
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=(
                    "Senha do cliente deve ter 6 ou mais caracteres, uma letra "
                    "maiúscula, uma letra minúscula, um número e um caractere especial"
                ),
                example="@Test123",
            ),
        },
        required=["email", "password"],
    )
    responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "access_token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Token de autenticação"
                ),
                "refresh_token": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Token de atualização de autenticação",
                ),
                "expires_in": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Tempo de expiração do token",
                ),
            },
        ),
        400: "Erro de validação",
        401: "Erro de autenticação",
        500: "Erro interno do servidor",
    }


class ConfirmCodeToResetPasswordCustomerDoc:
    tags = (["customer"],)
    operation_description = "Confirmação de redefinição de senha"
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "code": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Código de enviado pelo e-mail",
                example="123456",
            ),
            "email": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Email do cliente",
                example="john@doe.com",
            ),
        },
        required=["code", "email"],
    )
    responses = {
        204: "Sucesso",
        400: "Erro de validação",
        500: "Erro interno do servidor",
    }


class ForgetPasswordDoc:
    tags = (["customer"],)
    operation_description = "Solicitação de redefinição de senha"
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Email do cliente",
                example="john@doe.com",
            ),
        },
        required=["email"],
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
        500: "Erro interno do servidor",
    }


class NewPasswordDoc:
    tags = (["customer"],)
    operation_description = "Criação de nova senha"
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Email do cliente",
                example="john@doe.com",
            ),
        },
        required=["email"],
    )
    responses = {
        204: "Sucesso",
        400: "Erro de validação",
        500: "Erro interno do servidor",
    }


class RefreshLoginDoc:
    tags = (["customer"],)
    operation_description = "Autenticação de cliente"
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "access_token": openapi.Schema(
                type=openapi.TYPE_STRING, description="Token de autenticação"
            ),
            "refresh_token": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Token de atualização de autenticação",
            ),
        },
        required=["access_token", "refresh_token"],
    )
    responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "access_token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Token de autenticação"
                ),
                "refresh_token": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Token de atualização de autenticação",
                ),
                "expires_in": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Tempo de expiração do token",
                ),
            },
        ),
        400: "Erro de validação",
        401: "Erro de autenticação",
        500: "Erro interno do servidor",
    }
