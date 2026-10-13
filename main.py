
from fastapi import FastAPI
from src.utils.db import Base, Engine
from src.tasks.models import TaskModel

Base.metadata.create_all(Engine)

app = FastAPI(title="This is my Task Management Application")

@app.get("/home")
def greet ():
    return "Hi, Welcome to my Task Management Application"