from fastapi import HTTPException, status
from typing import Optional, Any, Dict


class AuthError(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, detail, headers)


class MyException(Exception):
    def __init__(self, message: str, status_code: int):
        self.status_code = status_code
        self.message = message

