from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Routinely API",
        default_version="v1",
        description="Documentação da API",
        license=openapi.License(name="Licença MIT"),
    ),
    public=True,
)

auths = {
    "Bearer": {
        "type": "apiKey",
        "name": "Authorization",
        "in": "header",
    },
}
