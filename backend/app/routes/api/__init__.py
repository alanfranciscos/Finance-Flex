"""Includes routes to FastAPI APIRouter."""

from fastapi import APIRouter

from backend.app.routes.v1 import user

endpoint_router = APIRouter()

endpoint_router.include_router(user.router, prefix="/user", tags=["User"])
