import uvicorn
from fastapi import FastAPI
from api.Create_conversation.routes import create_conversation_router
from api.Chat.routes import chat_router
from api.User.routes import user_router

import database
from database import create_tables
import models

app = FastAPI()


@app.on_event("startup")
async def startup():
    print("Connecting database...")
    await database.database.connect()
    models.models.Base.metadata.create_all(bind=database.engine)
    print("Sucessfully connnected")


@app.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(create_conversation_router)
app.include_router(chat_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
