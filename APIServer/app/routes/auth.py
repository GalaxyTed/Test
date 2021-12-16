from datetime import datetime, timedelta
import re
import bcrypt
import jwt

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.common.consts import JWT_SECRET, JWT_ALGORITHM
from Database.conn import database
from Database.schema import Users
from app.models.model import UserRegister, UserLogin, UserToken

router = APIRouter(prefix="/auth")

@router.post("/join")
async def register(reg_info: UserRegister, session: Session = Depends(database.session)):
    # 등록 할 email, password 값 유무 확인
    if not reg_info.email or not reg_info.password:
        return convert_jsonResponse(400, description="Email and PW must be provided")
    elif not checkEmailFormat(reg_info.email) : 
        return convert_jsonResponse(400, description="Check Email Format")
    # 동일한 Email이 존재하는지 확인 
    if isExistEmail(reg_info.email):
        return convert_jsonResponse(400, description="EMAIL_EXISTS")
    # Password 암호화 후 User Insert
    hash_pw = bcrypt.hashpw(reg_info.password.encode("utf-8"), bcrypt.gensalt())
    Users.create(session, auto_commit=True, password=hash_pw, email=reg_info.email, name=reg_info.name)
    return convert_jsonResponse(200,description="OK")

@router.post("/login")
async def login(login_info :UserLogin):
    is_exist = isExistEmail(login_info.email)
    if not login_info.email or not login_info.password:
        return convert_jsonResponse(400,description="Email and PW must be provided")
    if not is_exist:
        return convert_jsonResponse(400,description="NO_MATCH_USER")
    user = Users.get(email=login_info.email)
    is_verified = bcrypt.checkpw(login_info.password.encode("utf-8"), user.password.encode("utf-8"))
    if not is_verified:
        return convert_jsonResponse(400,description="NO_MATCH_USER")
    token = f"Bearer {create_access_token(data=UserToken.from_orm(user).dict(exclude={'password'}))}"
    return convert_jsonResponse(200, description="Success",token=token)


def isExistEmail(email: str):
    check_user = Users.get(email=email)
    if check_user:
        return True
    return False

def checkEmailFormat(email:str):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+[.]?\w{2,3}$'
    valid = re.search(regex, email)
    if valid:
        return True
    return False


def create_access_token(*, data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def convert_jsonResponse(status_code, **kwargs):
    content = dict(status_code=status_code)
    for key, val in kwargs.items():
        content[key] = val
    return JSONResponse(status_code=status_code, content=content)




