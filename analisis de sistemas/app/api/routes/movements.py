from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db
from app.models.movement import Movement
from app.schemas.movement import MovementCreate, MovementOut
from app.services.inventory_service import create_movement

router = APIRouter(prefix="/movements", tags=["movements"])

@router.post("", response_model=MovementOut, status_code=201)
def create_movement_endpoint(payload: MovementCreate, db: Session = Depends(get_db)):
    mv = create_movement(db, payload)
    return mv

@router.get("", response_model=List[MovementOut])
def list_movements(
    db: Session = Depends(get_db),
    product_id: Optional[int] = None,
    location_id: Optional[int] = None,
    type: Optional[str] = Query(None, pattern="^(IN|OUT|ADJUST)$"),
    page: int = Query(1, ge=1),
    size: int = Query(100, ge=1, le=500),
):
    stmt = select(Movement)
    if product_id is not None:
        stmt = stmt.where(Movement.product_id == product_id)
    if location_id is not None:
        stmt = stmt.where(Movement.location_id == location_id)
    if type is not None:
        stmt = stmt.where(Movement.type == type)
    stmt = stmt.order_by(Movement.created_at.desc()).offset((page - 1) * size).limit(size)
    return db.execute(stmt).scalars().all()
