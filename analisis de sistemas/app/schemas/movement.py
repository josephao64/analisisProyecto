from pydantic import BaseModel, condecimal, constr
from typing import Optional, Literal

MovementType = Literal["IN", "OUT", "ADJUST"]

class MovementCreate(BaseModel):
    product_id: int
    location_id: int
    type: MovementType
    quantity: condecimal(gt=0, max_digits=12, decimal_places=3)
    reason: constr(min_length=3, max_length=120)
    reference: Optional[constr(max_length=120)] = None

class MovementOut(MovementCreate):
    id: int
    class Config:
        from_attributes = True
