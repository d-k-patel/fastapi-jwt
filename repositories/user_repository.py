from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from db import get_db
from models import User
from schemas import UserRequest
from utils.auth import get_password_hash


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_users(self) -> List[User]:
        return self.db.query(User).all()

    def create_user(self, user: UserRequest) -> User:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            **user.model_dump(exclude={"password"}),
            password=hashed_password,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user(self, id: int) -> User:
        return self.db.query(User).filter(User.id == id).first()

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def delete_user(self, id: int) -> None:
        self.db.query(User).filter(User.id == id).delete()
        self.db.commit()

    def update_user(self, id: int, user_data: UserRequest) -> User:
        db_user = self.get_user(id)
        if db_user:
            user_dict = user_data.model_dump(exclude={"password"})
            for key, value in user_dict.items():
                setattr(db_user, key, value)
            if user_data.password:
                hashed_pasword = get_password_hash(user_data.password)
                setattr(db_user, "password", hashed_pasword)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)
