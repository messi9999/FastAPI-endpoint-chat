from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import io

from database import database, engine, get_db_session
from models.models import User

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session

from Schemas.UserSchema import UserSchema

user_router = APIRouter()


@user_router.post(
    "/users",
    response_model=None,
)
async def create_user(body: UserSchema, db: Session = Depends(get_db_session)):
    try:
        user = User(username=body.username, conversations=body.conversations)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists")
