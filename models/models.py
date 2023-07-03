import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    conversations = relationship("Conversation")
    articles = relationship("Article")
    created_at = Column(DateTime, default=datetime.datetime.now)


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    url = Column(String)
    userId = Column(Integer, ForeignKey("users.id"))
    createdAt = Column(DateTime, default=datetime.datetime.now)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey("users.id"))
    articleId = Column(Integer, ForeignKey("articles.id"))
    article = Column(String)
    messages = relationship("Message")
    startedAt = Column(DateTime, default=datetime.datetime.now)
    endedAt = Column(DateTime)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_question = Column(String)
    ChatGPT = Column(String)
    conversationId = Column(Integer, ForeignKey("conversations.id"))
    sentAt = Column(DateTime, default=datetime.datetime.now)
