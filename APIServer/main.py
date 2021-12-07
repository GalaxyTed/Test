import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from starlette.responses import JSONResponse
from fastapi import FastAPI
from typing import Optional

from Database import dao

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test/")
def read_test():
    return {"status": "0000"}

@app.get("/login/")
def read_item(email: Optional[str] = None, password: Optional[str] = None):
    try:
        result = dao.select_user(email,password)
    except:
        result = {"status": "9999"} 
    return JSONResponse(result)

@app.get("/user/")
def read_item(email: Optional[str] = None):
    try:
        result = dao.select_user(email)
    except:
        result = {"status": "9999"} 
    return JSONResponse(result)

@app.get("/secession/")
def read_item(email: Optional[str] = None):
    try:
        result = dao.delete_user(email)
    except:
        result = {"status": "9999"} 
    return JSONResponse(result)


@app.get("/join/")
def read_item(email: Optional[str] = None, password: Optional[str] = None, name: Optional[str] = None):
    try:
        result = dao.insert_user(email,password,name)
    except:
        result = {"status": "9999"}
    return JSONResponse(result)

@app.get("/xangle/notice/")
def read_item():
    try:
        result = dao.select_notice()
    except:
        result = {"status": "9999"}
    return JSONResponse(result)

@app.get("/klayswap/assets/")
def read_item(currency: Optional[str] = None):
    try:
        result = dao.select_assets(currency)
    except:
        result = {"status": "9999"}
    return JSONResponse(result)

@app.get("/klayswap/candles/")
def read_item(currency: Optional[str] = None, count: Optional[int] = 1,interval_type: Optional[str] = None, interval: Optional[int] = 1):
    try:
        result = dao.select_candles(currency, count ,interval_type, interval)
    except:
        result = {"status": "9999"}
    return JSONResponse(result)