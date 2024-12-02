from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.products import models, schemas


async def get_all_products(db: AsyncSession):
    query = select(models.Product)
    result = await db.execute(query)
    return result.scalars().all()


async def get_product_by_id(db: AsyncSession, product_id: int):
    query = select(models.Product).where(models.Product.id == product_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    query = insert(models.Product).values(product.model_dump()).returning(models.Product.id)
    result = await db.execute(query)
    await db.commit()
    product_id = result.scalar_one()

    query = select(models.Product).filter(models.Product.id == product_id)
    db_product = await db.execute(query)
    product = db_product.scalars().first()

    return product


async def update_product(
    db: AsyncSession, product_id: int, product_data: schemas.ProductUpdate
):
    product = await get_product_by_id(db, product_id)

    if product:
        for key, value in product_data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        await db.commit()
        await db.refresh(product)
        return product

    return None


async def update_partial_product(db: AsyncSession, product_id: int, product_data: dict):
    product = await get_product_by_id(db, product_id)

    if not product:
        return None

    for key, value in product_data.items():
        if value is not None:
            setattr(product, key, value)

    await db.commit()
    await db.refresh(product)

    return product


async def delete_product(db: AsyncSession, product_id: int):
    product = await get_product_by_id(db, product_id)

    if not product:
        return None

    await db.delete(product)
    await db.commit()
    return True
