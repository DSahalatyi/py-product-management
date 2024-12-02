from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status

from src.main import app


@pytest.mark.asyncio
async def test_list_products():
    mock_products = [
        {
            "id": 1,
            "name": "Product 1",
            "description": "Desc 1",
            "price": "100",
            "inventory": 1,
            "created_at": datetime.now().isoformat(),
        },
        {
            "id": 2,
            "name": "Product 2",
            "description": "Desc 2",
            "price": "50",
            "inventory": 1,
            "created_at": datetime.now().isoformat(),
        },
    ]

    with patch(
        "src.products.crud.get_all_products", AsyncMock(return_value=mock_products)
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("api/v1/products/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_products


@pytest.mark.asyncio
async def test_retrieve_product_found():
    mock_product = {
        "id": 1,
        "name": "Product 1",
        "description": "Desc 1",
        "price": "100",
        "inventory": 1,
        "created_at": datetime.now().isoformat(),
    }

    with patch(
        "src.products.crud.get_product_by_id", AsyncMock(return_value=mock_product)
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("api/v1/products/1/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_product


@pytest.mark.asyncio
async def test_retrieve_product_not_found():
    with patch("src.products.crud.get_product_by_id", AsyncMock(return_value=None)):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("api/v1/products/999/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Product not found"}


@pytest.mark.asyncio
async def test_update_product_success():
    mock_product = {
        "id": 1,
        "name": "Product 1",
        "description": "Desc 1",
        "price": "100",
        "inventory": 1,
        "created_at": datetime.now().isoformat(),
    }

    with patch(
        "src.products.crud.update_product", AsyncMock(return_value=mock_product)
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.put(
                "api/v1/products/1/",
                json={
                    "name": "Product 1",
                    "description": "Desc 1",
                    "price": "100",
                    "inventory": 1,
                },
            )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_product


@pytest.mark.asyncio
async def test_update_product_not_found():
    with patch("src.products.crud.update_product", AsyncMock(return_value=None)):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.put(
                "api/v1/products/999/", json={
                    "name": "Product 1",
                    "description": "Desc 1",
                    "price": "100",
                    "inventory": 1,
                }
            )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Product not found"}


@pytest.mark.asyncio
async def test_partial_update_product_success():
    mock_product = {
        "id": 1,
        "name": "Product 1",
        "description": "Desc 1",
        "price": "100",
        "inventory": 1,
        "created_at": datetime.now().isoformat(),
    }

    with patch(
        "src.products.crud.update_partial_product", AsyncMock(return_value=mock_product)
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.patch(
                "api/v1/products/1/", json={"name": "Partially Updated Product"}
            )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_product


@pytest.mark.asyncio
async def test_partial_update_product_not_found():
    with patch(
        "src.products.crud.update_partial_product", AsyncMock(return_value=None)
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.patch(
                "api/v1/products/999/", json={"name": "Non-existent Product"}
            )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Product not found"}


@pytest.mark.asyncio
async def test_delete_product_success():
    with patch("src.products.crud.delete_product", AsyncMock(return_value=True)):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.delete("api/v1/products/1/")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_product_not_found():
    with patch("src.products.crud.delete_product", AsyncMock(return_value=None)):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.delete("api/v1/products/999/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Product not found"}
