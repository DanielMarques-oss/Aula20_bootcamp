from pydantic import BaseModel, EmailStr, field_validator, FieldValidationInfo
from enum import Enum
from datetime import datetime
from typing import Optional


class HeroCategoryBase(Enum):
    categoria1 = "Fire"
    categoria2 = "Water"
    categoria3 = "Wood"
    categoria4 = "Wind"

class HeroBase(BaseModel):
    name: str
    description: Optional[str] = None
    categoria: str
    email_heroi: EmailStr

    @field_validator("categoria", mode="before")
    def check_categoria(cls, v, info: FieldValidationInfo):
        if v is None:
            return v
        if v in [item.value for item in HeroCategoryBase]:
            return v
        raise ValueError(f"Categoria inválida: {info}")


class HeroCreate(HeroBase):
    pass


class HeroResponse(HeroBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class HeroUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    categoria: Optional[str] = None
    email_heroi: Optional[EmailStr] = None

    @field_validator("categoria", mode="before")
    def check_categoria(cls, v, info: FieldValidationInfo):
        if v is None:
            return v
        if v in [item.value for item in HeroCategoryBase]:
            return v
        raise ValueError(f"Categoria inválida: {info}")