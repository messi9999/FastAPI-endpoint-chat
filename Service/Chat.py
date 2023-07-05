from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import datetime

from models.models import Conversation, Message


# Get article from database
async def get_article(conversationId, db):
    conversation_data = (
        db.query(Conversation).filter(Conversation.id == conversationId).first()
    )
    print("Got article from database")
    return conversation_data.article


# Save message to database
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
        conversation_data = db.query(Conversation).get(conversationId)
        if conversation_data:
            conversation_data.endedAt = datetime.datetime.now()
            db.commit()
        return None
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Error")


# Get message history from database
async def get_chat_history(conversationId, db):
    try:
        conversation_data = (
            db.query(Message).filter(Message.conversationId == conversationId).all()
        )
        print("Got article from database")
        return conversation_data
    except:
        return ""
