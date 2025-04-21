from fastapi import FastAPI

from dobu_manager.lifespan import lifespan

app: FastAPI = FastAPI(lifespan=lifespan)
