from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
from config import dotenv_path
from people_also_ask.routes import router
from dotenv import load_dotenv
from importlib.metadata import version
from pathlib import Path
from people_also_ask.logger.logger import CustomizeLogger

load_dotenv(dotenv_path)

config_path = Path(__file__).with_name("logging_config.json")

def create_app() -> FastAPI:
    app = FastAPI(version=version("people-also-ask"), title="people-also-ask")
    logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger

    return app

app = create_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

def run():
    uvicorn.run(app, host="0.0.0.0", port=8080, access_log=True)

