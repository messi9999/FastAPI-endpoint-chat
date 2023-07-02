from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import io

chat_router = APIRouter()


@chat_router.post("/chat")
async def chat(request: Request):
    ##Get Request body
    body = await request.json()
    conversation_id = body["conversation_id"]
    message = body["message"]

    # Create stream of text
    text = "Hello"
    result = io.BytesIO(text.encode())

    return StreamingResponse(result, media_type="application/octet-stream")
