from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(String)

    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="blogs")

    def __repr__(self):
        return f"<Blog(id={self.id}, title={self.title}, content={self.content})>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    # relationships
    blogs = relationship("Blog", back_populates="author")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, password={self.password})>"
