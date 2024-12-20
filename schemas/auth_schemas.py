from pydantic import BaseModel, EmailStr, Field, ConfigDict


class RequestLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4, max_length=20)


class RequestSignupSchema(BaseModel):
    email: EmailStr
    name: str
    password: str = Field(min_length=4, max_length=20)


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserSchema
