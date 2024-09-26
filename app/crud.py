from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from datetime import datetime
from .schemas import OrderStatus


# Products CRUD
async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def get_products(db: AsyncSession):
    result = await db.execute(select(models.Product))
    return result.scalars().all()


async def get_product_by_id(db: AsyncSession, product_id: int):
    result = await db.execute(select(models.Product).where(models.Product.id == product_id))
    return result.scalar_one_or_none()


async def update_product(db: AsyncSession, product_id: int, product: schemas.ProductUpdate):
    db_product = await get_product_by_id(db, product_id)
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        await db.commit()
        await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: int):
    db_product = await get_product_by_id(db, product_id)
    if db_product:
        await db.delete(db_product)
        await db.commit()
    return db_product


# Orders CRUD
async def create_order(db: AsyncSession, order: schemas.OrderCreate) -> models.Order:
    db_order = models.Order(created_at=datetime.utcnow(), status=OrderStatus.processing)

    # Assuming order.items is a list of dictionaries with product_id and quantity
    for item in order.items:
        db_order_item = models.OrderItem(product_id=item.product_id, quantity=item.quantity)
        db_order.items.append(db_order_item)  # Add OrderItem to the Order

    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order


async def get_orders(db: AsyncSession):
    result = await db.execute(select(models.Order))
    return result.scalars().all()


async def get_order_by_id(db: AsyncSession, order_id: int):
    try:
        result = await db.execute(select(models.Order).where(models.Order.id == order_id))
        return result.scalar_one_or_none()
    except Exception as e:
        print(f"Error fetching order by ID {order_id}: {e}")
        return None



async def update_order_status(db: AsyncSession, order_id: int, status: str):
    try:
        db_order = await get_order_by_id(db, order_id)
        if db_order:
            db_order.status = status
            await db.commit()
            await db.refresh(db_order)
            return db_order
        else:
            print(f"Order with ID {order_id} not found.")
            return None
    except Exception as e:
        print(f"Error updating order status for order ID {order_id}: {e}")
        return None
