from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import get_db
from models import User
from repositories.user_repository import UserRepository, get_user_repository
from schemas import UserRequest, UserResponse
from utils import logger
from utils.auth import get_current_user

router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(get_current_user)]
)


@router.get(
    "/",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
def get_users(repo: UserRepository = Depends(get_user_repository)) -> List[User]:
    """
    Retrieve all users from the database.
    """
    return repo.get_users()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserRequest,
    repo: UserRepository = Depends(get_user_repository),
) -> User:
    """
    Create a new user in the database.
    """
    return repo.create_user(user)


@router.get(
    "/{id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_user(
    id: int,
    repo: UserRepository = Depends(get_user_repository),
) -> User:
    """
    Retrieve a specific user by its ID.
    """
    user = repo.get_user(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )
    return user


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    id: int,
    repo: UserRepository = Depends(get_user_repository),
):
    """
    Delete a specific user by its ID.
    """
    repo.delete_user(id)
    return None


@router.put(
    "/{id}/",
    response_model=UserResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def update_user(
    id: int,
    request: UserRequest,
    repo: UserRepository = Depends(get_user_repository),
):
    """
    Update a specific user by its ID.
    """
    user = repo.update_user(id, request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )
    return user
