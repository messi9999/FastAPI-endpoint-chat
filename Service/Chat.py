from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import datetime

from models.models import Conversation, Message


async def get_article(conversationId, db):
    conversation_data = (
        db.query(Conversation).filter(Conversation.id == conversationId).first()
    )
    print("Got article from database")
    return conversation_data.article


async def save_message(user_question, ChatGPT, conversationId, db):
    try:
        print("Saving message to database")
        message = Message(
            user_question=user_question, ChatGPT=ChatGPT, conversationId=conversationId
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        print("Message successfuly Saved")
        print("Saving endedAt field in Conversation...")
        conversation_data = db.query(Conversation).get(conversationId)
        if conversation_data:
            conversation_data.endedAt = datetime.datetime.now()
            db.commit()
        return None
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Error")
