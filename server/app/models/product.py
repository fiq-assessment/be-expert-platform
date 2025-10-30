from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductIn(BaseModel):
    """Product input model"""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=2000)
    priceCents: int = Field(..., ge=0)
    stock: int = Field(..., ge=0)
    category: str = Field(..., min_length=1)

class ProductOut(BaseModel):
    """Product output model"""
    id: str
    name: str
    description: str
    priceCents: int
    stock: int
    category: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None

