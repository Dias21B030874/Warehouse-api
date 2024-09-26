import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
@pytest.mark.asyncio
async def test_create_order():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        product_data = {"name": "Test Product", "price": 100, "stock": 50}
        product_response = await ac.post("/products", json=product_data)
        assert product_response.status_code == 200

        order_data = {"items": [{"product_id": product_response.json()["id"], "quantity": 2}]}
        response = await ac.post("/orders", json=order_data)
        assert response.status_code == 200

        order = response.json()
        assert "id" in order
        assert order["items"] == order_data["items"]



@pytest.mark.asyncio
async def test_get_orders():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/orders")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        if response.json():
            assert "id" in response.json()[0]
            assert "items" in response.json()[0]
