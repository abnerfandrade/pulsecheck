import pytest


@pytest.mark.asyncio
async def test_list_services(async_client):
    response = await async_client.get("/services/")
    print("aqui", response.json())
    assert response.status_code == 200
