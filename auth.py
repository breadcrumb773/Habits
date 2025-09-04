from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import uvicorn

secret_user:str = "user"
secret_password:str = "password"

app = FastAPI()
basic: HTTPBasicCredentials = HTTPBasic()

@app.get("/who")
def get_user(creds: HTTPBasicCredentials = Depends(basic)):
    if (creds.username == secret_user and
        creds.password == secret_password):
        return {"username": creds.username, "password": creds.password}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Hay!")

if __name__ == "__main__":
    uvicorn.run("auth:app", host="localhost", port=8000, reload=True,)


# http -v --auth-type=basic -a me:secret http://127.0.0.1:8000/who