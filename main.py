
from fastapi import FastAPI
from src.utils.db import Base, Engine
from src.tasks.routers import task_routes

Base.metadata.create_all(Engine)

app = FastAPI(title="This is my Task Management Application")
app.include_router(task_routes)


@app.get("/home")
def greet ():
    return "Hi, Welcome to my Task Management Application"
