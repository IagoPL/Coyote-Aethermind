from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="Aethermind API")
app.include_router(api_router)
