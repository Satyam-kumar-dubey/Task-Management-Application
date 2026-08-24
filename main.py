
from fastapi import FastAPI

app = FastAPI(title="This is my Task Management Application")

@app.get("/home")
def greet ():
    return "Hi, Welcome to my Task Management Application"