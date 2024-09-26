from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, dependencies

router = APIRouter()

# Создание заказа
@router.post("/orders", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: AsyncSession = Depends(dependencies.get_db)):
    try:
        return await crud.create_order(db, order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Получение списка заказов
@router.get("/orders", response_model=list[schemas.Order])
async def get_orders(db: AsyncSession = Depends(dependencies.get_db)):
    return await crud.get_orders(db)

# Получение заказа по ID
@router.get("/orders/{order_id}", response_model=schemas.Order)
async def get_order(order_id: int, db: AsyncSession = Depends(dependencies.get_db)):
    order = await crud.get_order_by_id(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Обновление статуса заказа
@router.patch("/orders/{order_id}/status", response_model=schemas.Order)
async def update_order_status(order_id: int, status: schemas.OrderUpdateStatus, db: AsyncSession = Depends(dependencies.get_db)):
    updated_order = await crud.update_order_status(db, order_id, status.status)
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order
