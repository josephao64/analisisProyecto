from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**payload.model_dump())
    db.add(product)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail="SKU already exists")
    db.refresh(product)
    return product

@router.get("", response_model=List[ProductOut])
def list_products(
    db: Session = Depends(get_db),
    search: Optional[str] = None,
    category: Optional[str] = None,
    active: Optional[bool] = None,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
):
    stmt = select(Product)
    if search:
        like = f"%{search}%"
        stmt = stmt.where(or_(Product.sku.ilike(like), Product.name.ilike(like)))
    if category:
        stmt = stmt.where(Product.category == category)
    if active is not None:
        stmt = stmt.where(Product.active == active)
    stmt = stmt.offset((page - 1) * size).limit(size)
    items = db.execute(stmt).scalars().all()
    return items

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(product, k, v)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="SKU already exists")
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return None
