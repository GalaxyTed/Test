
class StatusCode:
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405
    
class APIException(Exception):
    status_code: int
    description: str
    ex: Exception

    def __init__(self,status_code: int = StatusCode.HTTP_500, description: str = "UNKNOWN", ex: Exception = None):
        self.status_code = status_code
        self.description = description
        self.ex = ex
        super().__init__(ex)


class AlreayExistEmailException(APIException):
    def __init__(self, email: str = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            description=f"동일한 Email이 존재합니다. : email = {email}",
            ex=ex
        )

class NotAuthorized(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            description=f"로그인이 필요한 서비스 입니다.",
            ex=ex
        )
        
class TokenExpiredEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            description=f"세션이 만료되어 로그아웃 되었습니다.",
            ex=ex
        )

class TokenDecodeEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            description=f"비정상적인 접근입니다.",
            ex=ex
        )