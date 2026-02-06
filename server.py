import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router as api_router
from data.config import DEV, SERVER_HOST, SERVER_PORT


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger("uvicorn")
    app.state.logger = logger
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("server:app", reload=DEV, port=SERVER_PORT, host=SERVER_HOST)
