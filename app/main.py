from fastapi import FastAPI
from .models.base import Base
from .database.database import engine
from .controllers.user_controller import router as user_router

app = FastAPI()

app.include_router(user_router)

Base.metadata.create_all(bind=engine)