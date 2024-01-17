from typing import Dict

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.config.logs import logConfiguration
from app.config.settings import get_settings
from app.routes import api

app = FastAPI()
settings = get_settings()
logConfiguration()


def custom_openapi() -> Dict:
    """Define a custom OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        description="API",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {"type": "http", "scheme": "bearer"}
    }

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [
                {"HTTPBearer": []}
            ]

            if openapi_schema["paths"][path][method]["responses"].get("422"):
                openapi_schema["paths"][path][method]["responses"][
                    "400"
                ] = openapi_schema["paths"][path][method]["responses"]["422"]
                openapi_schema["paths"][path][method]["responses"].pop("422")

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(api.endpoint_router, prefix=settings.API_V1)
