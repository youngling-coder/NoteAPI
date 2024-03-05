from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import task, user, auth


app = FastAPI()
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)


app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)
