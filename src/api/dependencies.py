from utils.unitofwork import IUnitOfWork, UnitOfWork
from slowapi.util import get_remote_address
from typing import Annotated
from slowapi import Limiter
from fastapi import Depends

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
limiter = Limiter(key_func=get_remote_address)
