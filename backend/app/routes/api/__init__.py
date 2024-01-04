"""Includes routes to FastAPI APIRouter."""

from fastapi import APIRouter

from backend.app.routes.v1 import authentication, user

endpoint_router = APIRouter()

endpoint_router.include_router(user.router, prefix="/user", tags=["User"])
endpoint_router.include_router(
    authentication.router, prefix="/authentication", tags=["User"]
)
