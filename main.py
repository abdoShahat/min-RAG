from fastapi import FastAPI

app = FastAPI()   # we use app as decorator 


@app.get("/welcome")
def welcome():
    return {
        "Message":"Welcome ya "
    }