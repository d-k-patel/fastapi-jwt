from fastapi import FastAPI, Request

from db import Base, engine
from routers import auth, blog, user
from utils import logger

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)


@app.get("/")
def root(request: Request) -> dict:
    """
    Root endpoint that returns a simple greeting.

    Returns:
        dict: A dictionary containing a greeting message.
    """
    logger.info(f"request received: {request.url}")
    return {"hello": "world"}
