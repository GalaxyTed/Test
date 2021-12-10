import json
from datetime import datetime, timedelta
import bcrypt
import jwt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.common.consts import JWT_SECRET, JWT_ALGORITHM
from Database.conn import db
from Database.schema import Users
from app.models.model import Token, UserToken, UserRegister

router = APIRouter(prefix="/auth")


@router.post("/register", status_code=201, response_model=Token)
async def register(reg_info: UserRegister, session: Session = Depends(db.session)):
    """
    `회원가입 API`\n
    :param sns_type:
    :param reg_info:
    :param session:
    :return:
    """
    
    is_exist = await is_email_exist(reg_info.email)
    if not reg_info.email or not reg_info.pw:
        return JSONResponse(status_code=400, content=dict(msg="Email and PW must be provided'"))
    if is_exist:
        return JSONResponse(status_code=400, content=dict(msg="EMAIL_EXISTS"))
    
    hash_pw = bcrypt.hashpw(reg_info.pw.encode("utf-8"), bcrypt.gensalt())
    new_user = Users.create(session, auto_commit=True, pw=hash_pw, email=reg_info.email)
    token = dict(Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(new_user).dict(exclude={'pw', 'marketing_agree'}),)}")
    return token



@router.post("/login", status_code=200)
async def login(user_info: UserRegister):
    is_exist = await is_email_exist(user_info.email)
    if not user_info.email or not user_info.pw:
        return JSONResponse(status_code=400, content=dict(status=400, description="Email and PW must be provided'"))
    if not is_exist:
        return JSONResponse(status_code=400, content=dict(status=400, description="NO_MATCH_USER"))
    
    user = Users.get(email=user_info.email)
    is_verified = bcrypt.checkpw(user_info.pw.encode("utf-8"), user.pw.encode("utf-8"))
    if not is_verified:
        return JSONResponse(status_code=400, content=dict(status=400, description="NO_MATCH_USER"))

    result_data = dict()
    result_data["status"] = "200";
    result_data["authorization"] = f"Bearer {create_access_token(data=UserToken.from_orm(user).dict(exclude={'pw'}),)}"
    result_data["data"] = [dict(email =user.email, name=user.name)]
    return result_data
  


async def is_email_exist(email: str):
    get_email = Users.get(email=email)
    if get_email:
        return True
    return False


def create_access_token(*, data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt
