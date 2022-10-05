from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post,users, auth,vote
from .config import settings

from app import database

#print(settings.database_username)

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware, allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1},
# {"title":"favourite foods", "content":"I like Pizza","id":2}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p["id"] == id:
#             return i

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message" : "Welcome to FastAPI!"}


