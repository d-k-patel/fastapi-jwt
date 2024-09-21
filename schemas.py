from typing import List

from pydantic import BaseModel, ConfigDict


class BlogBase(BaseModel):
    title: str
    content: str
    author_id: int


class BlogRequest(BlogBase):
    pass


class BlogResponse(BlogBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserRequest(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    blogs: List[BlogResponse]

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
