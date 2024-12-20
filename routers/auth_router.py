from typing import Annotated

from fastapi import APIRouter, Depends, Response, Request

from schemas.auth_schemas import RequestLoginSchema, RequestSignupSchema, AuthResponse, UserSchema
from services.user_service import UserService, user_service, current_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get('/me', response_model=UserSchema)
async def me(user: current_user):
    return user


@router.post("/login", response_model=AuthResponse)
async def login(
    response: Response,
    user_cred: RequestLoginSchema,
    users_service: Annotated[UserService, Depends(user_service)],
):
    tokens = await users_service.login_user(
        email=user_cred.email, password=user_cred.password
    )

    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True)

    response.set_cookie(key="access_token", value=tokens.access_token, httponly=True)

    return tokens


@router.post("/signup", response_model=AuthResponse)
async def signup(
    response: Response,
    user_cred: RequestSignupSchema,
    users_service: Annotated[UserService, Depends(user_service)],
):
    tokens = await users_service.create_user(
        email=user_cred.email, name=user_cred.name, password=user_cred.password
    )

    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True)

    response.set_cookie(key="access_token", value=tokens.access_token, httponly=True)

    return tokens


@router.get("/refresh", response_model=AuthResponse)
async def refresh_access_token(
    request: Request,
    response: Response,
    users_service: Annotated[UserService, Depends(user_service)],
):
    refresh_token = request.cookies.get("refresh_token")
    tokens = await users_service.refresh_access_token(refresh_token)

    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True)

    response.set_cookie(key="access_token", value=tokens.access_token, httponly=True)

    return tokens

@router.get("/logout")
async def logout(
    response: Response
):
    response.delete_cookie(key="refresh_token")
    response.delete_cookie(key="access_token")
    