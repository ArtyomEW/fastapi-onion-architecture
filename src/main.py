from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse
from core.exceptions import MyException
from starlette.requests import Request
from api.dependencies import limiter
from api.routers import all_routers
from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Упрощенный аналог Jira/Asana"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(MyException)
async def item_not_found_exception_handler(request: Request, exc: MyException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"{exc.message}"})


for router in all_routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
