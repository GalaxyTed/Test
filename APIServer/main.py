import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from dataclasses import asdict
from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware


from app.common.consts import EXCEPT_PATH_LIST, EXCEPT_PATH_REGEX
from app.common.config import conf
from app.middlewares.token_validator import access_control
from app.routes import index, auth, services, users
from Database.conn import db

API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)


def create_app():
    """
    앱 함수 실행
    :return:
    """
    
    app = FastAPI()
    config_dict = asdict(conf())
    db.init_app(app, **config_dict)
    
    app = FastAPI()


    # 미들웨어 정의
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    app.add_middleware(CORSMiddleware,allow_origins=conf().ALLOW_SITE,allow_credentials=True,allow_methods=["*"],allow_headers=["*"] )


    # 라우터 정의
    app.include_router(index.router)
    app.include_router(auth.router, tags=["Authentication"], prefix="/api")
    app.include_router(users.router, tags=["Users"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)])
 
    if conf().DEBUG:
        app.include_router(services.router, tags=["Services"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)])
    else:
        app.include_router(services.router, tags=["Services"], prefix="/api")
    return app
    

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
