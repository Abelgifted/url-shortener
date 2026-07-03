import os
from datetime import datetime
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr, HttpUrl, validator

from auth import (
    create_token,
    get_current_user,
    get_current_user_optional,
    hash_password,
    verify_password,
)
from database import (
    create_url,
    create_user,
    get_url,
    get_urls_for_user,
    get_user_by_email,
    increment_click,
    init_db,
)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

app = FastAPI(
    title="URL Shortener API",
    description="A professional URL shortening service",
    version="1.0.0",
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
    email: EmailStr
    password: str

    @validator("password")
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserResponse(BaseModel):
    id: int
    email: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ------------------------------------------------------------------
# User Routes
# ------------------------------------------------------------------

@app.post("/api/users/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate):
    existing_user = get_user_by_email(user.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists.")

    hashed_password = hash_password(user.password)

    user_id = create_user(user.email, hashed_password)

    return UserResponse(id=user_id, email=user.email)


@app.post("/api/users/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    user = get_user_by_email(credentials.email)

    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_token(user["id"])

    return TokenResponse(access_token=token)


# ------------------------------------------------------------------
# URL Routes
# ------------------------------------------------------------------

@app.post("/api/urls", response_model=URLResponse, status_code=201)
def shorten(
    request: CreateURLRequest,
    user_id: Optional[int] = Depends(get_current_user_optional),
):
    short_code = create_url(str(request.long_url), user_id=user_id)

    url = get_url(short_code)

    return URLResponse(
        short_code=short_code,
        long_url=str(request.long_url),
        short_url=f"{BASE_URL}/{short_code}",
        click_count=url["click_count"],
    )


@app.get("/api/urls")
def list_urls(user_id: int = Depends(get_current_user)):
    return get_urls_for_user(user_id)


@app.get("/api/urls/{short_code}/stats")
def stats(short_code: str):
    url = get_url(short_code)

    if url is None:
        raise HTTPException(status_code=404, detail="Short URL not found.")

    return url


# ------------------------------------------------------------------
# Root Route
# ------------------------------------------------------------------

@app.get("/")
def root():
    return {
        "service": "URL Shortener API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


# ------------------------------------------------------------------
# Redirect Route
# Keep LAST because it is the most generic route.
# ------------------------------------------------------------------

@app.get("/{short_code}")
def redirect(short_code: str):
    url = get_url(short_code)

    if url is None:
        raise HTTPException(status_code=404, detail="Short URL not found.")

    increment_click(short_code)

    return RedirectResponse(url=url["long_url"], status_code=302)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)