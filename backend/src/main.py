from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
# import uvicorn

from src.entity.base import init_db
from src.api import search

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    yield

app = FastAPI(
    description="spoonai 서버입니다.",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://spoonai.yeni-lab.org"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(search.router)

@app.get("/")
def read_root():
    return {"message": "spoonai 서버에 오신 것을 환영합니다."}

# if __name__ == "__main__":
#     uvicorn.run(app="src.main:app", reload=True)