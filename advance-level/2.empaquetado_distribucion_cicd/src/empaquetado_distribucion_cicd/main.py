from fastapi import FastAPI

app = FastAPI(title="Demo API", version="0.1.0")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello from empaquetado-distribucion-cicd!"}


@app.get("/items/{item_id}")
def get_item(item_id: int, name: str = "unknown") -> dict[str, object]:
    return {"item_id": item_id, "name": name}
