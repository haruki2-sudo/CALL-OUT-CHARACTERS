from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Association table: hero ↔ roles (many-to-many)
hero_roles = Table(
    "hero_roles",
    Base.metadata,
    Column("hero_id", Integer, ForeignKey("heroes.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    heroes = relationship("Hero", secondary=hero_roles, back_populates="roles")


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    nationality = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    notable_works = Column(Text, nullable=True)  # comma-separated
    image_url = Column(String, nullable=True)

    heroes = relationship("Hero", back_populates="actor")


class Hero(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    real_name = Column(String, nullable=True)
    attribute = Column(String, nullable=False)        # strength | agility | intelligence | universal
    attack_type = Column(String, nullable=False)      # melee | ranged
    complexity = Column(Integer, nullable=False)       # 1–3
    lore = Column(Text, nullable=True)
    faction = Column(String, nullable=True)            # Radiant | Dire | Neutral
    base_health = Column(Integer, nullable=True)
    base_mana = Column(Integer, nullable=True)
    base_armor = Column(Float, nullable=True)
    move_speed = Column(Integer, nullable=True)
    image_url = Column(String, nullable=True)

    actor_id = Column(Integer, ForeignKey("actors.id"), nullable=True)
    actor = relationship("Actor", back_populates="heroes")

    roles = relationship("Role", secondary=hero_roles, back_populates="heroes")
