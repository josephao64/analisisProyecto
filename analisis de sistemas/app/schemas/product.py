from pydantic import BaseModel, Field, constr, condecimal
from typing import Optional

class ProductBase(BaseModel):
    sku: constr(pattern=r'^[A-Za-z0-9\-_.]+$', min_length=3, max_length=32)
    name: constr(min_length=3, max_length=80)
    category: constr(min_length=2, max_length=50)
    unit: constr(min_length=2, max_length=20)
    min_stock: condecimal(ge=0, max_digits=12, decimal_places=3) = Field(default=0)
    price: condecimal(ge=0, max_digits=12, decimal_places=2) = Field(default=0)
    active: Optional[bool] = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    sku: Optional[constr(pattern=r'^[A-Za-z0-9\-_.]+$', min_length=3, max_length=32)] = None
    name: Optional[constr(min_length=3, max_length=80)] = None
    category: Optional[constr(min_length=2, max_length=50)] = None
    unit: Optional[constr(min_length=2, max_length=20)] = None
    min_stock: Optional[condecimal(ge=0, max_digits=12, decimal_places=3)] = None
    price: Optional[condecimal(ge=0, max_digits=12, decimal_places=2)] = None
    active: Optional[bool] = None

class ProductOut(ProductBase):
    id: int
    class Config:
        from_attributes = True
