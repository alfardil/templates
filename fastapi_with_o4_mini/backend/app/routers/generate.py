"""
Routes to invoke our LLM and generate responses.

"/test" tests our o4-mini implementation without streaming.
"/stream-test" tests our o4-mini implementation with streaming.

"""

from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.o4_mini_service import OpenAIo4Service


load_dotenv()

router = APIRouter(prefix="/generate", tags=["OpenAI"])

o4_service = OpenAIo4Service()


@router.get("/test")
async def test():
    """Test route for GPT implementation."""

    system_prompt: str = """
    You are a friendly chatbot. For now, simply return the data you recieve.
    """

    data: str = "This is the test endpoint for your o4 mini call."

    return o4_service.call_o4_api(system_prompt, data)


@router.get("/stream-test")
async def stream_test():
    """Test route for GPT's streaming implementation."""

    system_prompt: str = """
    You are a friendly chatbot. For now, simply return the data you recieve.
    """

    data: str = "This is the test endpoint for your o4 mini call."

    async def generate_stream():
        async for chunk in o4_service.call_o4_api_stream(system_prompt, data):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
