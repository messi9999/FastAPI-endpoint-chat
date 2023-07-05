from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

import io, traceback

from database import get_db_session
from Service.Chat import save_message, get_chat_history
from Schemas.ChatSchema import ChatSchema

from utils.utils import ChatGPT

from utils.save_article_pinecone import (
    searchquery,
    limit_string_tokens,
)

chat_router = APIRouter()


@chat_router.post("/chat")
async def chat(body: ChatSchema, db: Session = Depends(get_db_session)):
    # Get Request body
    conversationId = body.conversation_id
    message = body.message
    # Get article
    res = searchquery(
        message,
        "article-chat-" + str(conversationId),
    )
    summary = ""
    for r in res["matches"]:
        summary += r["metadata"]["content"]
    article = limit_string_tokens(summary, max_tokens=1000)

    # Get Chat history
    chat_array = await get_chat_history(conversationId=conversationId, db=db)
    chat_history = ""
    for chats in chat_array:
        chat_history = chats.ChatGPT + "\n" + chat_history
    chat_history = limit_string_tokens(chat_history, max_tokens=2500)
    # Get result answer from ChatGPT
    try:
        print("Waiting ChatGPT")
        answer = await ChatGPT(
            context=article, chat_history=chat_history, question=message
        )
        # answer = await openAI(prompt)
        print("Got answer from ChatGPT")
        print(answer)
    except Exception as e:
        print(traceback.format_exc())
        text = "OpenAI Failed!"
        result = io.BytesIO(text.encode())
        return StreamingResponse(result, media_type="application/octet-stream")
    # Create stream of text
    result = io.BytesIO(answer.encode())

    # Save message
    await save_message(
        user_question=message, ChatGPT=answer, conversationId=conversationId, db=db
    )

    return StreamingResponse(
        result,
        media_type="application/octet-stream",
    )
