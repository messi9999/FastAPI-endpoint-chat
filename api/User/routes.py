from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import io

from database import database, engine, get_db_session
from models.models import User

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session

from schemas.CreateUserSchema import CreateUserSchema

user_router = APIRouter()


@user_router.get("/health")
async def health():
    print("health request")
    return {"success": True}


@user_router.post(
    "/users",
    response_model=None,
)
async def create_user(body: CreateUserSchema, db: Session = Depends(get_db_session)):
    try:
        print("create user request")
        user = User(username=body.name)
        print(body.name)
        db.add(user)
        db.commit()
        db.refresh(user)
        print("create user success")
        return user
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists")
