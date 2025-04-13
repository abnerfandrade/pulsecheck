from fastapi import FastAPI
from app.routers import service_router, health_check_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(service_router.router)
app.include_router(health_check_router.router)
