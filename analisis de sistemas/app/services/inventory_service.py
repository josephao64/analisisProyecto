from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.product import Product
from app.models.location import Location
from app.models.stock import Stock
from app.models.movement import Movement
from app.schemas.movement import MovementCreate

def create_movement(db: Session, payload: MovementCreate) -> Movement:
    # Validar existencia de entidades
    product = db.execute(select(Product).where(Product.id == payload.product_id)).scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    location = db.execute(select(Location).where(Location.id == payload.location_id)).scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    qty = Decimal(payload.quantity)

    with db.begin():
        stock = db.execute(
            select(Stock).where(Stock.product_id == product.id, Stock.location_id == location.id).with_for_update()
        ).scalar_one_or_none()

        if not stock:
            stock = Stock(product_id=product.id, location_id=location.id, quantity=Decimal("0"))
            db.add(stock)
            db.flush()

        if payload.type == "OUT":
            if stock.quantity - qty < 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock for OUT movement")
            stock.quantity = stock.quantity - qty
        elif payload.type == "IN":
            stock.quantity = stock.quantity + qty
        elif payload.type == "ADJUST":
            # Ajuste se interpreta como sumar (positiva) o restar (si quisieras permitir negativo); aquí solo positiva.
            stock.quantity = stock.quantity + qty
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid movement type")

        movement = Movement(
            product_id=product.id,
            location_id=location.id,
            type=payload.type,
            quantity=qty,
            reason=payload.reason,
            reference=payload.reference
        )
        db.add(movement)
        db.flush()

    db.refresh(movement)
    return movement
