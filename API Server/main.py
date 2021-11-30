import test
from starlette.responses import JSONResponse
from fastapi import FastAPI
from typing import Optional


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
        result = test.select_user(email,password)
    except:
        result = {"status": "9999"} 
    return JSONResponse(result)

@app.get("/user/")
def read_item(email: Optional[str] = None):
    try:
        result = test.select_user(email)
    except:
        result = {"status": "9999"} 
    return JSONResponse(result)

@app.get("/secession/")
def read_item(email: Optional[str] = None):
    try:
        result = test.delete_user(email)
    except:
        result = {"status": "9999"} 
    return JSONResponse(result)


@app.get("/join/")
def read_item(email: Optional[str] = None, password: Optional[str] = None, name: Optional[str] = None):
    try:
        result = test.insert_user(email,password,name)
    except:
        result = {"status": "9999"}
    return JSONResponse(result)

@app.get("/xangle/notice/")
def read_item():
    try:
        result = test.select_notice()
    except:
        result = {"status": "9999"}
    return JSONResponse(result)