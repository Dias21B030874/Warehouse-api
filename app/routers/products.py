from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, dependencies

router = APIRouter()

# Создание товара
@router.post("/products", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, db: AsyncSession = Depends(dependencies.get_db)):
    return await crud.create_product(db, product)

# Получение списка товаров
@router.get("/products", response_model=list[schemas.Product])
async def get_products(db: AsyncSession = Depends(dependencies.get_db)):
    return await crud.get_products(db)

# Получение товара по ID
@router.get("/products/{product_id}", response_model=schemas.Product)
async def get_product(product_id: int, db: AsyncSession = Depends(dependencies.get_db)):
    product = await crud.get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Обновление товара по ID
@router.put("/products/{product_id}", response_model=schemas.Product)
async def update_product(product_id: int, product: schemas.ProductUpdate, db: AsyncSession = Depends(dependencies.get_db)):
    updated_product = await crud.update_product(db, product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

# Удаление товара по ID
@router.delete("/products/{product_id}", response_model=schemas.Product)
async def delete_product(product_id: int, db: AsyncSession = Depends(dependencies.get_db)):
    deleted_product = await crud.delete_product(db, product_id)
    if deleted_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product
