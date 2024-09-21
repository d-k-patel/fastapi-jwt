from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from db import get_db
from models import Blog
from schemas import BlogRequest


class BlogRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_blogs(self) -> List[Blog]:
        return self.db.query(Blog).all()

    def create_blog(self, blog: BlogRequest) -> Blog:
        db_blog = Blog(**blog.model_dump())
        self.db.add(db_blog)
        self.db.commit()
        self.db.refresh(db_blog)
        return db_blog

    def get_blog(self, id: int) -> Blog:
        return self.db.query(Blog).filter(Blog.id == id).first()

    def delete_blog(self, id: int) -> None:
        self.db.query(Blog).filter(Blog.id == id).delete()
        self.db.commit()

    def update_blog(self, id: int, blog_data: BlogRequest) -> Blog:
        db_blog = self.get_blog(id)
        if db_blog:
            blog_dict = blog_data.model_dump()
            for key, value in blog_dict.items():
                setattr(db_blog, key, value)
            self.db.commit()
            self.db.refresh(db_blog)
        return db_blog


def get_blog_repository(db: Session = Depends(get_db)) -> BlogRepository:
    return BlogRepository(db)
