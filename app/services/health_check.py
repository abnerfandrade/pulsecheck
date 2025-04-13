import httpx
from loguru import logger


async def check_service(url: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)

        return {"status": response.status_code, "success": response.status_code == 200}

    except Exception as e:
        logger.error(f"Health check failed for {url}: {str(e)}")
        return {"status": 0, "success": False}
