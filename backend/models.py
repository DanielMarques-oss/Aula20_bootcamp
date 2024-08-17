from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base


class HeroModel(Base):
    __tablename__ = "heros"  # esse será o nome da tabela

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    categoria = Column(String, index=True)
    email_heroi = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), index=True)