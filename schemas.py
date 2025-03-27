from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class ExtractDataRequest(BaseModel):
    message: str = Field(..., description="A mensagem para extrair dados")

    model_config = {
        "json_schema_extra": {
            "example": {"message": "Extraia informações importantes deste texto."}
        }
    }


class ExtractDataResponse(BaseModel):
    text: Dict[str, Any] = Field(..., description="Os dados extraídos em formato JSON")


class TextResponse(BaseModel):
    text: str = Field(..., description="O texto extraído")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Descrição do erro")
