from fastapi import FastAPI

app = FastAPI(title="Derivativ", version="0.1.0")


@app.get("/")
def hello_world():
    return {"message": "Hello World!"}
