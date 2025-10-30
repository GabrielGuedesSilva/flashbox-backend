from uuid import UUID

from pydantic import BaseModel


class AuthTokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class AuthUserCreateSchema(BaseModel):
    refresh_token: str
    user_id: UUID


class AuthUserUpdateSchema(BaseModel):
    refresh_token: str


class AuthUserResponseSchema(BaseModel):
    user_id: UUID
    access_token: str
    refresh_token: str


class UserCredentialsSchema(BaseModel):
    email: str
    password: str
