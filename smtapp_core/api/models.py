"""
Model management endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from pydantic import BaseModel

from config.settings import get_settings, get_toml_config
from services.model_service import ModelService

router = APIRouter()


class ModelInfo(BaseModel):
    """Model information schema"""
    name: str
    provider: str
    context_length: int
    available: bool


@router.get("/models", response_model=List[ModelInfo])
async def list_models():
    """
    List all available models
    """
    model_service = ModelService()
    models = await model_service.list_available_models()
    
    return [
        ModelInfo(
            name=model["name"],
            provider=model["provider"],
            context_length=model.get("context_length", 4096),
            available=model.get("available", False)
        )
        for model in models
    ]


@router.get("/models/ollama")
async def list_ollama_models():
    """
    List Ollama models
    """
    model_service = ModelService()
    try:
        models = await model_service.get_ollama_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Ollama service unavailable: {str(e)}"
        )


@router.post("/models/ollama/pull/{model_name}")
async def pull_ollama_model(model_name: str):
    """
    Pull an Ollama model
    """
    model_service = ModelService()
    try:
        result = await model_service.pull_ollama_model(model_name)
        return {"message": f"Model {model_name} pulled successfully", "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error pulling model: {str(e)}"
        )

