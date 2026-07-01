from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
import hashlib

from database import (
    init_db,
    create_url,
    get_url,
    increment_click,
    get_urls_for_user,
    create_user,
    get_user_by_email
)

app = FastAPI(
    title="URL Shortener API",
    description="A professional URL shortening service",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    init_db()


# ------------------------------------------------------------------
# Pydantic Models
# ------------------------------------------------------------------

class CreateURLRequest(BaseModel):
    long_url: HttpUrl
    expires_at: Optional[datetime] = None


class URLResponse(BaseModel):
    short_code: str
    long_url: str
    short_url: str
    click_count: int


class UserCreate(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str


# ------------------------------------------------------------------
# User Routes
# ------------------------------------------------------------------

@app.post(
    "/api/users/register",
    response_model=UserResponse,
    status_code=201
)
def register(user: UserCreate):

    existing_user = get_user_by_email(user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    hashed_password = hashlib.sha256(
        user.password.encode()
    ).hexdigest()

    user_id = create_user(
        user.email,
        hashed_password
    )

    return UserResponse(
        id=user_id,
        email=user.email
    )


# ------------------------------------------------------------------
# URL Routes
# ------------------------------------------------------------------

@app.post(
    "/api/urls",
    response_model=URLResponse,
    status_code=201
)
def shorten(request: CreateURLRequest):

    short_code = create_url(
        str(request.long_url)
    )

    url = get_url(short_code)

    return URLResponse(
        short_code=short_code,
        long_url=str(request.long_url),
        short_url=f"http://localhost:8000/{short_code}",
        click_count=url["click_count"]
    )


@app.get("/api/urls/{short_code}/stats")
def stats(short_code: str):

    url = get_url(short_code)

    if url is None:

        raise HTTPException(
            status_code=404,
            detail="Short URL not found."
        )

    return url


# ------------------------------------------------------------------
# Redirect Route
# Keep LAST because it is the most generic route.
# ------------------------------------------------------------------

@app.get("/{short_code}")
def redirect(short_code: str):

    url = get_url(short_code)

    if url is None:

        raise HTTPException(
            status_code=404,
            detail="Short URL not found."
        )

    increment_click(short_code)

    return RedirectResponse(
        url=url["long_url"],
        status_code=302
    )


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )