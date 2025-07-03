import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException


load_dotenv()


app = FastAPI()


db = {}


@app.get("/")
def read_root():
    """Returns a welcome message."""
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    """Returns an item from the database."""
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("API_PORT", 8000)))
