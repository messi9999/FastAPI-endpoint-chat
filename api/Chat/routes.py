from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from database import get_db_session
from Service.Chat import get_article, save_message
from Schemas.ChatSchema import ChatSchema

from utils import openAI

chat_router = APIRouter()


@chat_router.post("/chat")
async def chat(body: ChatSchema, db: Session = Depends(get_db_session)):
    # Get Request body
    conversationId = body.conversation_id
    message = body.message
    # Get article
    article = await get_article(conversationId=conversationId, db=db)

    # Create prompt
    prompt = """
{}
Please answer to bellow question based on above article! (Don't include any annotation)
{}
    """.format(
        article, message
    )
    # Get result answer from ChatGPT
    try:
        print("Waiting ChatGPT")
        answer = await openAI(prompt)
        print("Got answer from ChatGPT")
    except:
        text = "OpenAI Failed!"
        result = io.BytesIO(text.encode())
        return StreamingResponse(result, media_type="application/octet-stream")
    # Save message
    await save_message(
        user_question=message, ChatGPT=answer, conversationId=conversationId, db=db
    )
    # Create stream of text
    result = io.BytesIO(answer.encode())

    return StreamingResponse(result, media_type="application/octet-stream")
