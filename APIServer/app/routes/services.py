from fastapi import APIRouter
from starlette.requests import Request


router = APIRouter(prefix='/services')

@router.get('')
async def get_all_services(request: Request):
    result =dict(your_email=request.state.user.email)
    return result