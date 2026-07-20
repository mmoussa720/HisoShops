from fastapi import HTTPException, status


class AuthrError(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, detail: str="Could not validate credentials"):
        super().__init__(
            status_code=self.status_code,
            detail=detail
        )


class NotAuthorizedError(AuthrError):
    status_code = status.HTTP_401_UNAUTHORIZED


class LoginError(AuthrError):
    status_code = status.HTTP_401_UNAUTHORIZED
