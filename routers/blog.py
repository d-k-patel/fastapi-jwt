from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models import Blog
from repositories.blog_repository import BlogRepository, get_blog_repository
from schemas import BlogRequest, BlogResponse
from utils import logger
from utils.auth import get_current_user

router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@router.get(
    "/",
    response_model=list[BlogResponse],
    status_code=status.HTTP_200_OK,
)
def get_blogs(repo: BlogRepository = Depends(get_blog_repository)) -> List[Blog]:
    """
    Retrieve all blogs from the database.

    Args:
        db (Session): The database session.

    Returns:
        list[BlogResponse]: A list of all blogs.
    """
    return repo.get_blogs()


@router.post(
    "/",
    response_model=BlogResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_blog(
    blog: BlogRequest,
    repo: BlogRepository = Depends(get_blog_repository),
) -> Blog:
    """
    Create a new blog entry in the database.

    Args:
        blog (BlogRequest): The blog data to be created.
        db (Session): The database session.

    Returns:
        Blog: The created blog entry.
    """
    return repo.create_blog(blog)


@router.get(
    "/{id}",
    response_model=BlogResponse,
    status_code=status.HTTP_200_OK,
)
def get_blog(
    id: int,
    repo: BlogRepository = Depends(get_blog_repository),
) -> Blog:
    """
    Retrieve a specific blog by its ID.

    Args:
        id (int): The ID of the blog to retrieve.
        db (Session): The database session.

    Returns:
        Blog: The requested blog entry.

    Raises:
        HTTPException: If the blog is not found.
    """

    blog = repo.get_blog(id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found!",
        )
    return blog


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_blog(
    id: int,
    repo: BlogRepository = Depends(get_blog_repository),
) -> None:
    """
    Delete a specific blog by its ID.

    Args:
        id (int): The ID of the blog to delete.
        db (Session): The database session.

    Returns:
        None
    """

    repo.delete_blog(id)
    return None


@router.put(
    "/{id}/",
    response_model=BlogResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def update_blog(
    id: int,
    request: BlogRequest,
    repo: BlogRepository = Depends(get_blog_repository),
) -> Blog:
    """
    Update a specific blog by its ID.

    Args:
        id (int): The ID of the blog to update.
        request (BlogRequest): The updated blog data.
        db (Session): The database session.

    Returns:
        Blog: The updated blog entry.

    Raises:
        HTTPException: If the blog is not found.
    """

    blog = repo.update_blog(id, request)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found!",
        )
    return blog
