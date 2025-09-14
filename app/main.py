from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from typing import Any


from app.web import user, habit
from app.data.errors import Missing, Duplicate
from app.models.errors import UserNameError

import utils

app = FastAPI()

@app.exception_handler(Missing)
async def missing_handler(_:Request, exc:Missing):
    return JSONResponse(status_code=404,content={"detail":exc.msg})

@app.exception_handler(Duplicate)
async def duplicate_handler(_:Request, exc:Duplicate):
    return JSONResponse(status_code=409, content={"detail":exc.msg})

@app.exception_handler(UserNameError)
async def usernameerror_handler(_:Request, exc:UserNameError):
    return JSONResponse(status_code=404, content={"detail":exc.msg})

app.include_router(user.router)
app.include_router(habit.router)

@app.get("/")
def top():
    return {"message": "This is the top page"}


@app.get("/echo/{thing}")
def echo(thing):
    return f"echoing {thing}"

if __name__ == "__main__":
    uvicorn.run("app.main:app",host="127.0.0.1",port=8000, reload=True) 