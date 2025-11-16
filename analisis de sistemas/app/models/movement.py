from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base

MovementType = Enum("IN", "OUT", "ADJUST", name="movement_type")

class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="RESTRICT"), nullable=False)
    type = Column(MovementType, nullable=False)
    quantity = Column(Numeric(12, 3), nullable=False)
    reason = Column(String(120), nullable=False)
    reference = Column(String(120), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    product = relationship("Product", back_populates="movements")
    location = relationship("Location", back_populates="movements")
