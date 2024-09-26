import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        product_data = {
            "name": "Test Product",
            "description": "A description of the test product",
            "price": 100,
            "quantity": 50,
            "stock": 50
        }
        response = await ac.post("/products", json=product_data)

        assert response.status_code == 200

        assert response.json()["name"] == "Test Product"

        assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_products():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/products")
        assert response.status_code == 200
        assert isinstance(response.json(), list)