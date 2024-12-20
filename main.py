# from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.auth_router import router as auth_router
from routers.form_router import router as form_router
# from models import db, Base


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with db.engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield


# app = FastAPI(lifespan=lifespan)
app = FastAPI()
app.include_router(auth_router)
app.include_router(form_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping", tags=["test"])
async def ping():
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
