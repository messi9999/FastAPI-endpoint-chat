from fastapi import APIRouter, Depends
from utils.utils import get_content
from Service.Create_conversation import create_Conversation

from sqlalchemy.orm import Session
from database import get_db_session
from Schemas.CreateConversationSchema import CreateConversatiionSchema

from utils.save_article_pinecone import (
    embedding_openAI,
    chunk_content,
    embedding_config,
    embedding_to_pinecone,
)

create_conversation_router = APIRouter()


@create_conversation_router.post("/create_conversation")
async def create_conversation(
    body: CreateConversatiionSchema, db: Session = Depends(get_db_session)
):
    # Get request body data
    userId = body.user_id
    url = body.url

    # Create conversation_id
    conversation_id = 0

    result = await get_content(url)

    if result["status_code"] == 200:
        article_content = result["content"]
        article_title = result["title"]
        # Save article
        conversation_id = await create_Conversation(
            userId=userId, title=article_title, content=article_content, url=url, db=db
        )
        chunks = chunk_content(article_content, 500)
        embedded = embedding_openAI(chunks)
        vectors = embedding_config(chunks, embedded)
        embedding_to_pinecone(vectors, "article-chat-" + str(conversation_id))
        # Return conversation id
        return {"conversation_id": conversation_id}

    else:
        # Return error
        return {"conversation_id": result["content"]}
