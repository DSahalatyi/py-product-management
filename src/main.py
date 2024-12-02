from fastapi import FastAPI

from src.products.routers import router

app = FastAPI()

api_version_prefix = "/api/v1"

app.include_router(router, prefix=api_version_prefix)

@app.get("/")
async def root():
    return {"message": "Hello World"}
