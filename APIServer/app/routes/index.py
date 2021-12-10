from datetime import datetime

from fastapi import APIRouter
from starlette.responses import Response
from starlette.requests import Request

router = APIRouter()


@router.get("/")
async def index():
    current_time = datetime.now()
    return Response(f"Welcom to API Server (Time: {current_time.strftime('%Y.%m.%d %H:%M:%S')})")

@router.get("/test")
async def test(request: Request):
    """
    ELB 상태 체크용 API
    :return:
    """
    print("state.user", request.state.user)
    current_time = datetime.utcnow()
    return Response(f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})")