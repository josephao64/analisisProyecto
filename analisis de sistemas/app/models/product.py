from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, func, Index
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(32), unique=True, nullable=False, index=True)
    name = Column(String(80), nullable=False)
    category = Column(String(50), nullable=False)
    unit = Column(String(20), nullable=False)
    min_stock = Column(Numeric(12, 3), nullable=False, default=0)
    price = Column(Numeric(12, 2), nullable=False, default=0)
    active = Column(Boolean, nullable=False, default=True, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    stocks = relationship("Stock", back_populates="product", cascade="all, delete-orphan")
    movements = relationship("Movement", back_populates="product", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_products_sku_unique", "sku", unique=True),
    )
