from pydantic import BaseModel
from typing import List, Optional


class RoleOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ActorBase(BaseModel):
    name: str
    nationality: Optional[str] = None
    bio: Optional[str] = None
    notable_works: Optional[str] = None
    image_url: Optional[str] = None


class ActorOut(ActorBase):
    id: int

    class Config:
        from_attributes = True


class HeroBase(BaseModel):
    name: str
    real_name: Optional[str] = None
    attribute: str
    attack_type: str
    complexity: int
    lore: Optional[str] = None
    faction: Optional[str] = None
    base_health: Optional[int] = None
    base_mana: Optional[int] = None
    base_armor: Optional[float] = None
    move_speed: Optional[int] = None
    image_url: Optional[str] = None


class HeroOut(HeroBase):
    id: int
    actor: Optional[ActorOut] = None
    roles: List[RoleOut] = []

    class Config:
        from_attributes = True
