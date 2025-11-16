from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate, LocationOut

router = APIRouter(prefix="/locations", tags=["locations"])

@router.post("", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
def create_location(payload: LocationCreate, db: Session = Depends(get_db)):
    loc = Location(**payload.model_dump())
    db.add(loc)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Location code already exists")
    db.refresh(loc)
    return loc

@router.get("", response_model=List[LocationOut])
def list_locations(
    db: Session = Depends(get_db),
    active: Optional[bool] = None,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
):
    stmt = select(Location)
    if active is not None:
        stmt = stmt.where(Location.active == active)
    stmt = stmt.offset((page - 1) * size).limit(size)
    items = db.execute(stmt).scalars().all()
    return items

@router.get("/{location_id}", response_model=LocationOut)
def get_location(location_id: int, db: Session = Depends(get_db)):
    loc = db.get(Location, location_id)
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    return loc

@router.put("/{location_id}", response_model=LocationOut)
def update_location(location_id: int, payload: LocationUpdate, db: Session = Depends(get_db)):
    loc = db.get(Location, location_id)
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(loc, k, v)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Location code already exists")
    db.refresh(loc)
    return loc

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    loc = db.get(Location, location_id)
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(loc)
    db.commit()
    return None
