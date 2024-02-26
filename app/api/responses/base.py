"""Base response class for the API."""

from fastapi.responses import JSONResponse
from starlette import status


class BaseResponse:
    """Base response class."""

    @staticmethod
    def success_response(status_code=status.HTTP_200_OK, message="Success", data=None):
        """
        The function `success_response` returns a JSON response with a success status code and message.

        :param status_code: The `status_code` parameter is used to specify the HTTP status code for the
        response. By default, it is set to `status.HTTP_200_OK`, which indicates a successful response
        :param message: The `message` parameter is a string that represents the success message that will be
        included in the response. By default, it is set to "Success"
        :return: a JSONResponse object with a success status code and message.
        """
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "success",
                "message": message,
                "data": data,
            },
        )

    @staticmethod
    def error_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Error", data=None):
        """
        The function `error_response` returns a JSON response with a success status code and message.

        :param status_code: The `status_code` parameter is used to specify the HTTP status code for the
        response. By default, it is set to `status.HTTP_500_INTERNAL_SERVER_ERROR`, which indicates a error response.
        :param message: The `message` parameter is a string that represents the error message that will be
        included in the response. By default, it is set to "Error"
        :return: a JSONResponse object with a error status code and message.
        """
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "error",
                "message": message,
                "data": data,
            },
        )
