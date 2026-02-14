from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models import init_db
from app.api import messages_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(messages_router)

@app.on_event("startup")
async def startup_event():
    print("Iniciando aplicação...")
    init_db()
    print("Aplicação iniciada com sucesso.")

@app.get("/")
async def root():
    return {
        "message": "Bem-vindo ao MessageFlow AI!",
        "version": settings.APP_VERSION,
        "docs": "/docs"   
    }