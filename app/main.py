from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Returns a welcome message."""
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """Returns an item with its ID and an optional query parameter."""
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
