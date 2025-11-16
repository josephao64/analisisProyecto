from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Index
from sqlalchemy.orm import relationship
from app.core.database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(80), nullable=False)
    active = Column(Boolean, nullable=False, default=True, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    stocks = relationship("Stock", back_populates="location", cascade="all, delete-orphan")
    movements = relationship("Movement", back_populates="location", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_locations_code_unique", "code", unique=True),
    )
