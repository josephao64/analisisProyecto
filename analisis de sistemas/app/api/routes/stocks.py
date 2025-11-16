from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.core.database import get_db
from app.models.stock import Stock
from app.models.product import Product
from app.schemas.stock import StockOut

router = APIRouter(prefix="/stocks", tags=["stocks"])

@router.get("", response_model=List[StockOut])
def list_stocks(
    db: Session = Depends(get_db),
    product_id: Optional[int] = None,
    location_id: Optional[int] = None,
    low_stock_only: Optional[bool] = False,
    page: int = Query(1, ge=1),
    size: int = Query(100, ge=1, le=500),
):
    stmt = select(Stock)
    if product_id is not None:
        stmt = stmt.where(Stock.product_id == product_id)
    if location_id is not None:
        stmt = stmt.where(Stock.location_id == location_id)
    if low_stock_only:
        # join with Product to compare min_stock
        stmt = stmt.join(Product, Product.id == Stock.product_id).where(Stock.quantity < Product.min_stock)
    stmt = stmt.offset((page - 1) * size).limit(size)
    return db.execute(stmt).scalars().all()
