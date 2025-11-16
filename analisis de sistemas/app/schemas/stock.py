from pydantic import BaseModel, condecimal
from typing import Optional

class StockOut(BaseModel):
    id: int
    product_id: int
    location_id: int
    quantity: condecimal(ge=0, max_digits=12, decimal_places=3)
    class Config:
        from_attributes = True
