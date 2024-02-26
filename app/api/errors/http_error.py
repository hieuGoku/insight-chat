"""HTTP Error handler for the API."""

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    The function `http_error_handler` handles HTTP exceptions by returning a JSON response with the
    error details and status code.

    :param request: The `request` parameter is an instance of the `Request` class, which represents the
    incoming HTTP request being handled by the server. It contains information about the request, such
    as the HTTP method, headers, query parameters, and body
    :type request: Request
    :param exc: The parameter `exc` is an instance of the `HTTPException` class. It represents the
    exception that occurred during the handling of an HTTP request. It contains information about the
    error, such as the status code and the error message
    :type exc: HTTPException
    :return: a JSONResponse object.
    """
    if request:
        pass

    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)
