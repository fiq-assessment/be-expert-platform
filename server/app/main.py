from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.db import init_db
from .routers import admin, stats

app = FastAPI(
    title="Admin Platform API",
    version="1.0.0",
    description="Interview exercise: Expert BE - RBAC + Caching + N+1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(admin.router)
app.include_router(stats.router)

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    await init_db()

@app.get("/health")
async def health():
    return {"ok": True, "service": "admin-platform-api"}

