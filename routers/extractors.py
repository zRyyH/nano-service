from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
from middleware.auth import verify_token
from schemas import ExtractDataRequest, ExtractDataResponse, TextResponse, ErrorResponse
from services.pdf_service import extract_text_from_pdf
from services.xlsx_service import extract_text_from_xlsx
from services.image_service import extract_text_from_image
from services.data_service import extract_important_data
from concurrent.futures import ThreadPoolExecutor
import asyncio


# Criar executor de threads
executor = ThreadPoolExecutor(max_workers=10)


# Obter loop de execução
loop = asyncio.get_running_loop()


# Criar router com autenticação
router = APIRouter(
    prefix="/api", tags=["extractors"], dependencies=[Depends(verify_token)]
)


@router.post(
    "/extract-text-from-xlsx",
    response_model=TextResponse,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
    summary="Extract text from XLSX file",
    description="Extracts all text content from an Excel XLSX file",
)
async def extract_xlsx_endpoint(
    file: UploadFile = File(...),
    sheet_index: int = 0,
    start_row: int = 1,
    end_row: int = None,
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty file name")

    content = await file.read()

    try:
        result = await loop.run_in_executor(
            executor, extract_text_from_xlsx, content, sheet_index, start_row, end_row
        )

        return JSONResponse(content=result, status_code=status.HTTP_200_OK)

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing XLSX file: {str(e)}"
        )


@router.post(
    "/extract-text-from-pdf",
    response_model=TextResponse,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
    summary="Extract text from PDF file",
    description="Extracts all text content from a PDF file",
)
async def extract_pdf_endpoint(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty file name")

    content = await file.read()

    try:
        text = await loop.run_in_executor(executor, extract_text_from_pdf, content)
        return {"text": text}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing PDF file: {str(e)}"
        )


@router.post(
    "/extract-text-from-image",
    response_model=Dict[str, Any],
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
    summary="Extract text from image",
    description="Extracts text content from an image using Google Cloud Vision API",
)
async def extract_image_endpoint(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty file name")

    content = await file.read()

    try:
        text = await loop.run_in_executor(executor, extract_text_from_image, content)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")


@router.post(
    "/extract-important-data",
    response_model=Dict[str, Any],
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
    summary="Extract important data from text",
    description="Extracts structured data from text using OpenAI API",
)
async def extract_data_endpoint(request: ExtractDataRequest):
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="message parameter is required")

        result = await loop.run_in_executor(
            executor, extract_important_data, request.message
        )
        return {"text": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting data: {str(e)}")
