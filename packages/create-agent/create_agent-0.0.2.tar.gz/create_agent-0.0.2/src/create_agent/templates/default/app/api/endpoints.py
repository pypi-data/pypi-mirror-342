import time

from app.api.dependencies import verify_api_key
from app.api.models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    HealthCheckResponse,
)
from app.config import settings
from app.services.chat_service import ChatService
from app.utils.logging import logger
from fastapi import APIRouter, BackgroundTasks, Depends

router = APIRouter(tags=["RAG"])


@router.post(
    "/chat/completions",
    response_model=ChatCompletionResponse,
    summary="Create Chat Completion",
    description="Process chat completions in OpenAI format with optional streaming.",
)
async def chat_completions(
    request: ChatCompletionRequest,
    _background_tasks: BackgroundTasks,
    _api_key: str = Depends(verify_api_key),
):
    """Process chat completions in OpenAI format."""
    model_name = request.model or settings.LLM_MODEL
    logger.info(f"Received chat request for model: {model_name}")
    chat_service = ChatService()
    return await chat_service.chat(request)


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health Check",
    description="Check the health status of the API",
)
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "timestamp": time.time()}
