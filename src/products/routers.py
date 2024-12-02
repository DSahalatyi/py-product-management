from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from src.products import schemas, crud

router = APIRouter()


@router.get("/products/", response_model=List[schemas.Product])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_products(db)


@router.get("/products/{product_id}/", response_model=schemas.Product)
async def retrieve_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud.get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("/products/", response_model=schemas.Product)
async def create_product(
    product: schemas.ProductCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_product(db, product)


@router.put("/products/{product_id}/", response_model=schemas.Product)
async def update_product(
    product: schemas.ProductUpdate, product_id: int, db: AsyncSession = Depends(get_db)
):
    product = await crud.update_product(db, product_id, product)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.patch("/products/{product_id}/", response_model=schemas.Product)
async def partial_update_product(
    product: schemas.ProductPartialUpdate,
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    update_data = product.model_dump(exclude_unset=True)
    product = await crud.update_partial_product(db, product_id, update_data)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.delete("/products/{product_id}/", status_code=204)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud.delete_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}
