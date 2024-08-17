from sqlalchemy.orm import Session
from schemas import HeroUpdate, HeroCreate
from models import HeroModel


def get_hero(db: Session, hero_id: int):
    """
    funcao que recebe um id e retorna somente ele
    """
    return db.query(HeroModel).filter(HeroModel.id == hero_id).first()


def get_heros(db: Session):
    """
    funcao que retorna todos os elementos
    """
    return db.query(HeroModel).all()


def create_hero(db: Session, hero: HeroCreate):
    db_hero = HeroModel(**hero.model_dump())
    db.add(db_hero)
    db.commit()
    db.refresh(db_hero)
    return db_hero


def delete_hero(db: Session, hero_id: int):
    db_hero = db.query(HeroModel).filter(HeroModel.id == hero_id).first()
    db.delete(db_hero)
    db.commit()
    return db_hero


def update_hero(db: Session, hero_id: int, hero: HeroUpdate):
    db_hero = db.query(HeroModel).filter(HeroModel.id == hero_id).first()

    if db_hero is None:
        return None
    if hero.name is not None:
        db_hero.name = hero.name
    if hero.description is not None:
        db_hero.description = hero.description
    if hero.categoria is not None:
        db_hero.categoria = hero.categoria
    if hero.email_heroi is not None:
        db_hero.email_heroi = hero.email_heroi

    db.commit()
    return db_hero