import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
    # conversations = relationship("Conversation", back_populates="user")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    createdAt = Column(DateTime, default=datetime.datetime.now)
    conversations = relationship("Conversation", back_populates="article")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    startedAt = Column(DateTime, default=datetime.datetime.now)
    endedAt = Column(DateTime)
    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="conversations")
    articleId = Column(Integer, ForeignKey("articles.id"))
    article = relationship("Article", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String)
    sentAt = Column(DateTime, default=datetime.datetime.now)
    conversationId = Column(Integer, ForeignKey("conversations.id"))
    conversation = relationship("Conversation", back_populates="messages")
