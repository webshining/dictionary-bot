from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from data.config import DIR

from .routes import router as api_router

app = FastAPI()
app.mount("/static", StaticFiles(directory=f"{DIR}/api/static"), name="static")
app.include_router(api_router)
