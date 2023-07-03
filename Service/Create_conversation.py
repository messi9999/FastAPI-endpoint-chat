from fastapi import HTTPException
from models.models import Article, Conversation
from sqlalchemy.exc import IntegrityError

import datetime


async def create_Conversation(userId, title, content, url, db):
    try:
        article = Article(userId=userId, url=url, title=title, content=content)
        db.add(article)
        db.commit()
        db.refresh(article)
        article_data = db.query(Article).filter(Article.userId == userId).first()
        conversation = Conversation(
            userId=userId,
            articleId=article_data.id,
            article=article_data.content,
            messages=[],
            endedAt=datetime.datetime.now(),
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        conversation_data = (
            db.query(Conversation)
            .filter(
                Conversation.userId == userId, Conversation.articleId == article_data.id
            )
            .first()
        )

        return conversation_data.id
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Error")
