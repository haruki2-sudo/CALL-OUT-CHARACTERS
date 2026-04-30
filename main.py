from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal, engine
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: seed the database
    db = SessionLocal()
    try:
        crud.seed_data(db)
    finally:
        db.close()
    yield
    # Shutdown: nothing to clean up for SQLite


app = FastAPI(
    title="🎮 Dota 2 Fanbase API",
    description="""
## Welcome to the **Dota 2 Fanbase API** 🗡️🔥

This API provides detailed information about Dota 2 heroes (characters) and the voice actors behind them.

### Features
- 🧙 **Get All Heroes** — Browse every hero in the Dota 2 universe
- 🔍 **Get a Specific Hero** — Fetch details about one hero by ID or name
- 🎙️ **Get Voice Actors** — Discover the actors who bring heroes to life

### Hero Attributes
- **Strength** 💪, **Agility** 🏹, **Intelligence** 🧠, **Universal** ⚡
    """,
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Dota 2 Fanbase",
        "url": "https://www.dota2.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─── Root ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "🎮 Welcome to the Dota 2 Fanbase API!",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "all_heroes": "/heroes",
            "hero_by_id": "/heroes/{hero_id}",
            "hero_by_name": "/heroes/name/{name}",
            "all_actors": "/actors",
            "actor_by_id": "/actors/{actor_id}",
            "heroes_by_actor": "/actors/{actor_id}/heroes",
        }
    }


# ─── Heroes ──────────────────────────────────────────────────────────────────

@app.get("/heroes", response_model=List[schemas.HeroOut], tags=["Heroes"])
def get_all_heroes(
    attribute: Optional[str] = None,
    role: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve **all Dota 2 heroes**.

    Optional filters:
    - **attribute**: `strength`, `agility`, `intelligence`, `universal`
    - **role**: `carry`, `support`, `initiator`, `jungler`, `pusher`, `durable`, `nuker`, `escape`, `disabler`
    """
    return crud.get_heroes(db, attribute=attribute, role=role, skip=skip, limit=limit)


@app.get("/heroes/name/{name}", response_model=schemas.HeroOut, tags=["Heroes"])
def get_hero_by_name(name: str, db: Session = Depends(get_db)):
    """
    Retrieve a **specific hero by name** (case-insensitive partial match).

    Example: `/heroes/name/invoker`
    """
    hero = crud.get_hero_by_name(db, name)
    if not hero:
        raise HTTPException(status_code=404, detail=f"Hero '{name}' not found")
    return hero


@app.get("/heroes/{hero_id}", response_model=schemas.HeroOut, tags=["Heroes"])
def get_hero_by_id(hero_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a **specific hero by ID**.
    """
    hero = crud.get_hero(db, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail=f"Hero with ID {hero_id} not found")
    return hero


# ─── Actors ──────────────────────────────────────────────────────────────────

@app.get("/actors", response_model=List[schemas.ActorOut], tags=["Actors"])
def get_all_actors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve **all voice actors** in the Dota 2 universe.
    """
    return crud.get_actors(db, skip=skip, limit=limit)


@app.get("/actors/{actor_id}", response_model=schemas.ActorOut, tags=["Actors"])
def get_actor_by_id(actor_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a **specific voice actor by ID**.
    """
    actor = crud.get_actor(db, actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail=f"Actor with ID {actor_id} not found")
    return actor


@app.get("/actors/{actor_id}/heroes", response_model=List[schemas.HeroOut], tags=["Actors"])
def get_heroes_by_actor(actor_id: int, db: Session = Depends(get_db)):
    """
    Retrieve **all heroes voiced by a specific actor**.
    """
    actor = crud.get_actor(db, actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail=f"Actor with ID {actor_id} not found")
    return crud.get_heroes_by_actor(db, actor_id)
