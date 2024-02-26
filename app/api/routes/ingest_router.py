"""Ingest router for the API"""

from fastapi import APIRouter, File, UploadFile

from app.api.responses.base import BaseResponse
from app.api.errors.error_message import BaseErrorMessage
from app.api.services.ingest_service import ingest_service
from app.logger.logger import custom_logger


router = APIRouter()


@router.post("/file")
async def ingest_file(file: UploadFile = File(...)):
    """
    ## Description
    The `ingest` function takes an uploaded file, reads its content, and passes it to an ingest service
    for further processing, returning the resulting documents.

    ## Parameters
    - **file**: The `file` parameter is of type `UploadFile`, which is a class provided by the FastAPI
    framework. It represents a file uploaded by the client as part of a multipart form data request. It
    contains information about the uploaded file, such as its filename and content.

    ## Returns
    The function `ingest` returns a list of documents (`docs`) if successful.
    """
    try:
        await file.seek(0)
        file_name = file.filename
        file_content = await file.read()

        docs = ingest_service.ingest_file(file_content, file_name)

        return docs

    except ValueError as e:
        custom_logger.debug(str(e))
        error_message: BaseErrorMessage = e.args[0]
        return BaseResponse.error_response(message=error_message.message)

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message="Internal Server Error")


@router.post("/url")
async def ingest_url(url: str):
    """
    ## Description
    The `ingest_url` function takes a URL, fetches the content at that URL, and passes it to an ingest
    service for further processing, returning the resulting documents.

    ## Parameters
    - **url**: The `url` parameter is of type `str` and represents the URL of the content to be ingested.

    ## Returns
    The function `ingest_url` returns a list of documents (`docs`) if successful.
    """
    try:
        docs = ingest_service.ingest_url(url)

        return docs

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message="Internal Server Error")


@router.get("/source")
async def get_sources():
    """Get all sources."""
    try:
        sources = ingest_service.get_sources()

        return BaseResponse.success_response(
            status_code=200, message="Sucessfully retrieved files", data=sources
        )

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message="Internal Server Error")


@router.get("/documents")
async def get_docs():
    """Get all documents."""
    try:
        docs = ingest_service.get_docs()

        return docs

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message="Internal Server Error")


@router.get("/documents/{source}")
async def get_docs_by_source(source: str):
    """Get documents by file name."""
    try:
        docs = ingest_service.get_docs_by_source(source)

        return docs

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message="Internal Server Error")


@router.delete("/documents/{source}")
async def delete_docs_by_source(source: str):
    """Delete documents by file name."""
    try:
        docs_ids_deleted = ingest_service.delete_docs_by_source(source)

        return BaseResponse.success_response(
            status_code=200,
            message=f"Successfully deleted documents with source: {source}, deleted count: {len(docs_ids_deleted)}",
            data=docs_ids_deleted,
        )

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message="Internal Server Error")


@router.delete("/documents")
async def delete_all_docs():
    """Delete all documents."""
    try:
        file_names_deleted = ingest_service.delete_all_docs()

        return BaseResponse.success_response(
            status_code=200,
            message=f"Successfully deleted all documents, deleted count: {len(file_names_deleted)}",
            data=file_names_deleted,
        )

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message="Internal Server Error")
