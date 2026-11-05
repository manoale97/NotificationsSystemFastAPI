from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes.users import router as users_router
from app.domain.errors import EmailAlreadyExistsError, UserNotFoundError
from app.infrastructure.database import create_db_and_tables


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    create_db_and_tables()
    yield


app = FastAPI(
    title="Notifications System API",
    description="API inicial con FastAPI y una arquitectura limpia ligera.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(
    _: Request, error: UserNotFoundError
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(error)})


@app.exception_handler(EmailAlreadyExistsError)
async def email_already_exists_handler(
    _: Request, error: EmailAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(error)})


app.include_router(users_router)
