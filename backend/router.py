from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas import HeroResponse, HeroUpdate, HeroCreate
from typing import List
from crud import (
    create_hero,
    get_heros,
    get_hero,
    delete_hero,
    update_hero,
)

router = APIRouter()


@router.post("/heros/", response_model=HeroResponse)
def create_hero_route(hero: HeroCreate, db: Session = Depends(get_db)):
    return create_hero(db=db, hero=hero)


@router.get("/heros/", response_model=List[HeroResponse])
def read_all_heros_route(db: Session = Depends(get_db)):
    heros = get_heros(db)
    return heros


@router.get("/heros/{hero_id}", response_model=HeroResponse)
def read_hero_route(hero_id: int, db: Session = Depends(get_db)):
    db_hero = get_hero(db, hero_id=hero_id)
    if db_hero is None:
        raise HTTPException(status_code=404, detail="hero not found")
    return db_hero


@router.delete("/heros/{hero_id}", response_model=HeroResponse)
def detele_hero_route(hero_id: int, db: Session = Depends(get_db)):
    db_hero = delete_hero(db, hero_id=hero_id)
    if db_hero is None:
        raise HTTPException(status_code=404, detail="hero not found")
    return db_hero


@router.put("/heros/{hero_id}", response_model=HeroResponse)
def update_hero_route(
    hero_id: int, hero: HeroUpdate, db: Session = Depends(get_db)
):  
    db_hero = update_hero(db, hero_id=hero_id, hero=hero)
    if db_hero is None:
        raise HTTPException(status_code=404, detail="hero not found")
    return db_hero

