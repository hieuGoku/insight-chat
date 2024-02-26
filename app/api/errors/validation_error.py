"""Validation Error handler for the API"""
from __future__ import annotations

from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def http422_error_handler(
    request: Request,
    exc: (RequestValidationError | ValidationError),
) -> JSONResponse:
    """
    The function `http422_error_handler` handles HTTP 422 errors by returning a JSON response with the
    validation errors.

    :param request: The `request` parameter is of type `Request` and represents the incoming HTTP
    request that caused the error
    :type request: Request
    :param exc: The `exc` parameter in the `http422_error_handler` function is of type
    `RequestValidationError` or `ValidationError`
    :type exc: (RequestValidationError | ValidationError)
    :return: a JSONResponse object.
    """
    if request:
        pass

    return JSONResponse(
        {"errors": exc.errors()},
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": f"{REF_PREFIX}ValidationError"},
    },
}
