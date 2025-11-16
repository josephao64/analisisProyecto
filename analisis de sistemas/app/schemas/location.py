from pydantic import BaseModel, constr
from typing import Optional

class LocationBase(BaseModel):
    code: constr(min_length=2, max_length=20)
    name: constr(min_length=2, max_length=80)
    active: Optional[bool] = True

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    code: Optional[constr(min_length=2, max_length=20)] = None
    name: Optional[constr(min_length=2, max_length=80)] = None
    active: Optional[bool] = None

class LocationOut(LocationBase):
    id: int
    class Config:
        from_attributes = True
