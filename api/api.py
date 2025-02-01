from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from data.config import DIR
from .routes import router as api_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=None)
app.mount("/static", StaticFiles(directory=f"{DIR}/api/static"), name="static")
app.include_router(api_router)
