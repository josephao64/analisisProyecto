from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(title="Inventory API", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(api_router)
