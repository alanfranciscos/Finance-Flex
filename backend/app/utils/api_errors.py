# Base imports
from __future__ import annotations

from typing import Any, Dict, Optional, Union

# Third-party imports
from fastapi import HTTPException

ErrorDetail = Optional[Union[str, Dict[str, str]]]


def raise_error_response(
    error: Union[Any, BaseException],
    detail: ErrorDetail = None,
    **args: Dict[str, Any],
) -> None:
    """Raise a HTTPException with a custom error."""
    error_body = dict(error.error)

    if detail is not None:
        error_body["detail"] = detail

    if args:
        error_body = {**error_body, **args}

    raise HTTPException(
        status_code=error.status_code,
        detail=error_body,
    )


class ErrorResourceInvalid:
    """Class that defines an error for an invalid resource."""

    status_code = 400

    error = {
        "type": "invalid_resource",
        "description": "The requested resource is invalid.",
    }


class ErrorResourceDataInvalid:
    """Class that defines an error for an invalid resource data."""

    status_code = 400

    error = {
        "type": "invalid_resource_data",
        "description": "The requested resource contains invalid data.",
    }


class ErrorResourceFormatInvalid:
    """Class that defines an error for an invalid resource format."""

    status_code = 400

    error = {
        "type": "invalid_resource_format",
        "description": "The requested resource contains invalid format.",
    }


class ErrorInternal:
    """Class that defines an error for an internal error."""

    status_code = 500

    error = {
        "type": "internal_error",
        "description": "An internal error has occurred "
        "while processing the request.",
    }


class NotFound:
    """Class that defines an error for a not found resource."""

    status_code = 404

    error = {
        "type": "not_found",
        "description": "The server can not find the requested resource.",
    }


class ErrorAuthorizationForbidden:
    """Class that defines an error for a forbidden request."""

    status_code = 403

    error = {
        "type": "not_found",
        "description": "The client does not have "
        "access rights to the content.",
    }


class ErrorAuthenticationInvalid:
    """Class that defines an error for an invalid authentication."""

    status_code = 401

    error = {
        "type": "invalid_authentication",
        "description": "The authentication key provided is invalid.",
    }


class DataAlreadyExists:
    """Class that defines an error for a data already exists."""

    status_code = 409

    error = {
        "type": "data_already_exists",
        "description": "The data already exist.",
    }


class GenericBadRequest:
    """Class that defines an error for a bad request."""

    def __init__(self, error: Optional[Dict] = None) -> None:
        self.status_code = 400
        self.error = (
            error
            if error
            else {
                "type": "invalid_resource",
                "description": "The requested resource is invalid.",
            }
        )
