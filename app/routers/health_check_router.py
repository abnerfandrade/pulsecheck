from fastapi import APIRouter, Query
from app.services.health_check import check_service
from app.schemas.health_check import HealthCheckRead

router = APIRouter(prefix="/health_check", tags=["HealthCheck"])


@router.get("/", response_model=HealthCheckRead)
async def check_status(
    url: str = Query(description="URL do serviço/site a ser verificado. " \
                                 "Deve informar o protocolo http no início, ex: https://")
):
    response = await check_service(url)

    return response
