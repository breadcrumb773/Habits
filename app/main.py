from fastapi import FastAPI
import uvicorn
from typing import Any

from web import explorer, creature

app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)

@app.get("/")
def top():
    return {"message": "This is the top page"}


@app.get("/echo/{thing}")
def echo(thing):
    return f"echoing {thing}"

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000, reload=True)


# $env:PYTHONPATH = "C:\main_projects\fastapi_test"