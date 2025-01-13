from utils.unitofwork import IUnitOfWork, UnitOfWork
from typing import Annotated
from fastapi import Depends

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
