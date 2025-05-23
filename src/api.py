from fastapi import Depends, FastAPI, Response
import bcrypt
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from typing import Annotated

from pydantic import BaseModel, Field

from src.db import (
    create_user,
    bootstrap,
    get_user_from_email,
    test_connection,
    update_user_with_id,
)
from src.models.User import User


app = FastAPI()
security = HTTPBasic()

bootstrap()


class UpdateRequest(BaseModel):
    """
    Request body for updating user information.
    """

    password: str | None = Field(min_length=8, default=None)
    last_name: str | None = Field(min_length=1, default=None)
    first_name: str | None = Field(min_length=1, default=None)


@app.get("/healthz")
async def health_check():
    """
    Health check endpoint.
    """
    res = test_connection()
    if res:
        return Response(status_code=200)
    return Response(status_code=503)


@app.post("/signup/")
async def signup(new_user: User):
    """
    Sign up a new user.
    """
    new_user.password = bcrypt.hashpw(
        new_user.password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    res = create_user(new_user)
    if res:
        return Response(status_code=201)
    return Response(status_code=503)


@app.get("/login/")
async def login(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """
    Log in a user.
    """
    user = get_user_from_email(credentials.username)
    if user is not None:
        if bcrypt.checkpw(
            credentials.password.encode("utf-8"), user.password.encode("utf-8")
        ):
            return Response(status_code=200)
    return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})


@app.get("/me")
async def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    """
    Get the current user.
    """
    user = get_user_from_email(credentials.username)
    if user is not None and bcrypt.checkpw(
        credentials.password.encode("utf-8"), user.password.encode("utf-8")
    ):
        return Response(status_code=200, content=user.__repr__())
    return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})


@app.put("/me")
async def update_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    new_user: UpdateRequest,
):
    """
    Update the current user.
    """
    user_from_db = get_user_from_email(credentials.username)
    if user_from_db is not None and bcrypt.checkpw(
        credentials.password.encode("utf-8"), user_from_db.password.encode("utf-8")
    ):
        res = update_user_with_id(
            user_from_db.id,
            User(
                first_name=(
                    new_user.first_name
                    if new_user.first_name
                    else user_from_db.first_name
                ),
                last_name=(
                    new_user.last_name if new_user.last_name else user_from_db.last_name
                ),
                password=(
                    bcrypt.hashpw(
                        new_user.password.encode("utf-8"), bcrypt.gensalt()
                    ).decode("utf-8")
                    if new_user.password
                    else user_from_db.password
                ),
            ),
        )
        if res:
            return Response(status_code=200)
    return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})
