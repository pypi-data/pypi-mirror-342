from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from dobu_manager.services.study_service import start_optuna_synchronizer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await start_optuna_synchronizer(60)
    yield
