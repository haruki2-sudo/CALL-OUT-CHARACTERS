from sqlalchemy.orm import Session
from models import Hero, Actor, Role
from typing import List, Optional


# ─── Seed Data ────────────────────────────────────────────────────────────────

SEED_ACTORS = [
    {
        "name": "David Scully",
        "nationality": "British",
        "bio": "British voice actor known for his iconic delivery of Invoker's spellcasting lines. One of the most recognizable voices in Dota 2.",
        "notable_works": "Invoker (Dota 2), Halo series, various animation projects",
        "image_url": "https://www.dota2.com/images/heroes/invoker/portrait.png",
    },
    {
        "name": "Will Tulin",
        "nationality": "American",
        "bio": "American voice actor and the voice behind Axe in Dota 2. Known for his booming, aggressive delivery.",
        "notable_works": "Axe (Dota 2), various video game and animation roles",
        "image_url": "https://www.dota2.com/images/heroes/axe/portrait.png",
    },
    {
        "name": "Kari Wahlgren",
        "nationality": "American",
        "bio": "Prolific American voice actress who brings life to several Dota 2 heroes including Lina and Luna.",
        "notable_works": "Lina (Dota 2), Luna (Dota 2), Rick and Morty, Family Guy",
        "image_url": "https://www.dota2.com/images/heroes/lina/portrait.png",
    },
    {
        "name": "Jim Foronda",
        "nationality": "American",
        "bio": "American voice actor known for voicing several Dota 2 heroes. His deep, gravelly tones define characters like Underlord.",
        "notable_works": "Underlord (Dota 2), Timbersaw (Dota 2), various anime dubs",
        "image_url": "https://www.dota2.com/images/heroes/underlord/portrait.png",
    },
    {
        "name": "Ellen McLain",
        "nationality": "American",
        "bio": "American soprano and voice actress, famous for GLaDOS in Portal. She voiced Omniknight in Dota 2.",
        "notable_works": "Omniknight (Dota 2), GLaDOS (Portal), Team Fortress 2",
        "image_url": "https://www.dota2.com/images/heroes/omniknight/portrait.png",
    },
    {
        "name": "Dave Fennoy",
        "nationality": "American",
        "bio": "Award-winning American voice actor with a legendary baritone voice, known for voicing Keeper of the Light.",
        "notable_works": "Keeper of the Light (Dota 2), The Walking Dead (Telltale), various games",
        "image_url": "https://www.dota2.com/images/heroes/keeper_of_the_light/portrait.png",
    },
    {
        "name": "Jon St. John",
        "nationality": "American",
        "bio": "The iconic voice of Duke Nukem also brings life to Dota 2's Dragon Knight with a commanding presence.",
        "notable_works": "Dragon Knight (Dota 2), Duke Nukem Forever, various video games",
        "image_url": "https://www.dota2.com/images/heroes/dragon_knight/portrait.png",
    },
    {
        "name": "Courtenay Taylor",
        "nationality": "American",
        "bio": "Award-winning voice actress known for her expressive range, voicing Templar Assassin in Dota 2.",
        "notable_works": "Templar Assassin (Dota 2), Jack (Mass Effect), Fallout 4",
        "image_url": "https://www.dota2.com/images/heroes/templar_assassin/portrait.png",
    },
]

SEED_HEROES = [
    {
        "name": "Invoker",
        "real_name": "Carl",
        "attribute": "intelligence",
        "attack_type": "ranged",
        "complexity": 3,
        "faction": "Radiant",
        "base_health": 560,
        "base_mana": 375,
        "base_armor": 1,
        "move_speed": 280,
        "lore": "In the history of Dota 2, Invoker stands alone as the most technically demanding hero. An immortal magus of impossible ego and unparalleled power, he believes himself to be the greatest intellect in the world.",
        "image_url": "https://www.dota2.com/images/heroes/invoker/portrait.png",
        "actor_name": "David Scully",
        "roles": ["Carry", "Nuker", "Disabler", "Escape", "Pusher"],
    },
    {
        "name": "Axe",
        "real_name": "Mogul Khan",
        "attribute": "strength",
        "attack_type": "melee",
        "complexity": 1,
        "faction": "Dire",
        "base_health": 720,
        "base_mana": 231,
        "base_armor": 2,
        "move_speed": 310,
        "lore": "In the Oglodi clan, the one who rises to Warchief is the one who can defeat all others. Mogul Khan didn't just defeat his rivals — he called out armies to come and fight him.",
        "image_url": "https://www.dota2.com/images/heroes/axe/portrait.png",
        "actor_name": "Will Tulin",
        "roles": ["Initiator", "Durable", "Disabler"],
    },
    {
        "name": "Lina",
        "real_name": "Lina Inverse",
        "attribute": "intelligence",
        "attack_type": "ranged",
        "complexity": 2,
        "faction": "Radiant",
        "base_health": 492,
        "base_mana": 387,
        "base_armor": 1,
        "move_speed": 290,
        "lore": "The older of two sisters gifted with elemental fire magic, Lina the Slayer outshines her sibling in both power and temper. Her fireballs have reduced armies to cinders.",
        "image_url": "https://www.dota2.com/images/heroes/lina/portrait.png",
        "actor_name": "Kari Wahlgren",
        "roles": ["Carry", "Support", "Nuker", "Disabler"],
    },
    {
        "name": "Luna",
        "real_name": "Luna Moonfang",
        "attribute": "agility",
        "attack_type": "ranged",
        "complexity": 1,
        "faction": "Radiant",
        "base_health": 560,
        "base_mana": 243,
        "base_armor": 3,
        "move_speed": 330,
        "lore": "Chosen by Selemene herself, Luna gave up her past life to serve as the Moon Rider — a divine warrior protecting the Nightsilver Woods.",
        "image_url": "https://www.dota2.com/images/heroes/luna/portrait.png",
        "actor_name": "Kari Wahlgren",
        "roles": ["Carry", "Pusher", "Nuker"],
    },
    {
        "name": "Underlord",
        "real_name": "Vrogros",
        "attribute": "strength",
        "attack_type": "melee",
        "complexity": 2,
        "faction": "Dire",
        "base_health": 720,
        "base_mana": 303,
        "base_armor": 4,
        "move_speed": 300,
        "lore": "From the Abyssal Horde, Underlord rules through fear and strength. His infernal gate can swallow armies and transport them to distant battlefields.",
        "image_url": "https://www.dota2.com/images/heroes/underlord/portrait.png",
        "actor_name": "Jim Foronda",
        "roles": ["Durable", "Disabler", "Initiator", "Nuker"],
    },
    {
        "name": "Omniknight",
        "real_name": "Purist Thunderwrath",
        "attribute": "strength",
        "attack_type": "melee",
        "complexity": 1,
        "faction": "Radiant",
        "base_health": 720,
        "base_mana": 267,
        "base_armor": 3,
        "move_speed": 290,
        "lore": "A veteran knight who devoted himself to the Omniscience, Purist Thunderwrath gave up personal glory to serve as a holy guardian, blessed with divine armor and healing.",
        "image_url": "https://www.dota2.com/images/heroes/omniknight/portrait.png",
        "actor_name": "Ellen McLain",
        "roles": ["Support", "Durable", "Disabler"],
    },
    {
        "name": "Keeper of the Light",
        "real_name": "Ezalor",
        "attribute": "intelligence",
        "attack_type": "ranged",
        "complexity": 2,
        "faction": "Radiant",
        "base_health": 492,
        "base_mana": 519,
        "base_armor": 0,
        "move_speed": 325,
        "lore": "The ancient Ezalor carries within him the primordial light of creation. Once an ethereal being of pure luminance, he now wanders the physical world in a senile, benevolent form.",
        "image_url": "https://www.dota2.com/images/heroes/keeper_of_the_light/portrait.png",
        "actor_name": "Dave Fennoy",
        "roles": ["Support", "Nuker", "Disabler", "Pusher"],
    },
    {
        "name": "Dragon Knight",
        "real_name": "Davion",
        "attribute": "strength",
        "attack_type": "melee",
        "complexity": 1,
        "faction": "Radiant",
        "base_health": 720,
        "base_mana": 243,
        "base_armor": 4,
        "move_speed": 290,
        "lore": "Davion the Dragon Knight slew an ancient dragon cursed with undeath, and in doing so took its soul into himself. He can now transform into a mighty dragon in battle.",
        "image_url": "https://www.dota2.com/images/heroes/dragon_knight/portrait.png",
        "actor_name": "Jon St. John",
        "roles": ["Carry", "Durable", "Pusher", "Initiator", "Disabler"],
    },
    {
        "name": "Templar Assassin",
        "real_name": "Lanaya",
        "attribute": "agility",
        "attack_type": "ranged",
        "complexity": 2,
        "faction": "Neutral",
        "base_health": 560,
        "base_mana": 195,
        "base_armor": 3,
        "move_speed": 310,
        "lore": "Lanaya came to the Templar Assassins seeking answers about her past. Instead she became a devoted protector of forbidden secrets, lurking in shadows with unmatched psionic blades.",
        "image_url": "https://www.dota2.com/images/heroes/templar_assassin/portrait.png",
        "actor_name": "Courtenay Taylor",
        "roles": ["Carry", "Escape", "Nuker", "Pusher"],
    },
    {
        "name": "Juggernaut",
        "real_name": "Yurnero",
        "attribute": "agility",
        "attack_type": "melee",
        "complexity": 2,
        "faction": "Radiant",
        "base_health": 560,
        "base_mana": 243,
        "base_armor": 4,
        "move_speed": 305,
        "lore": "The last survivor of the Bleeding Hollow tribe, Yurnero wears a mask that has never been removed. His omnislash is a whirlwind of death that few can survive.",
        "image_url": "https://www.dota2.com/images/heroes/juggernaut/portrait.png",
        "actor_name": None,
        "roles": ["Carry", "Pusher", "Escape", "Nuker"],
    },
    {
        "name": "Anti-Mage",
        "real_name": "Magina",
        "attribute": "agility",
        "attack_type": "melee",
        "complexity": 2,
        "faction": "Radiant",
        "base_health": 560,
        "base_mana": 195,
        "base_armor": 3,
        "move_speed": 315,
        "lore": "From a family of mages, Magina returned to find his kin slaughtered by the demon Chaos Knight. He now crusades against magic itself, burning mana from enemies with every strike.",
        "image_url": "https://www.dota2.com/images/heroes/antimage/portrait.png",
        "actor_name": None,
        "roles": ["Carry", "Escape", "Nuker"],
    },
    {
        "name": "Crystal Maiden",
        "real_name": "Rylai",
        "attribute": "intelligence",
        "attack_type": "ranged",
        "complexity": 1,
        "faction": "Radiant",
        "base_health": 492,
        "base_mana": 387,
        "base_armor": -1,
        "move_speed": 275,
        "lore": "The younger sister of Lina, Rylai's ice magic is so uncontrollable that she had to be exiled to the frozen tundra. She brings Frostbite and Freezing Fields to her allies' aid.",
        "image_url": "https://www.dota2.com/images/heroes/crystal_maiden/portrait.png",
        "actor_name": None,
        "roles": ["Support", "Disabler", "Nuker"],
    },
]


# ─── CRUD Helpers ─────────────────────────────────────────────────────────────

def get_or_create_role(db: Session, name: str) -> Role:
    role = db.query(Role).filter(Role.name == name.lower()).first()
    if not role:
        role = Role(name=name.lower())
        db.add(role)
        db.flush()
    return role


def seed_data(db: Session):
    if db.query(Hero).count() > 0:
        return  # Already seeded

    actor_map = {}
    for a in SEED_ACTORS:
        actor = Actor(**a)
        db.add(actor)
        db.flush()
        actor_map[a["name"]] = actor

    for h in SEED_HEROES:
        h = h.copy()  # never mutate the module-level constant
        actor_name = h.pop("actor_name")
        role_names = h.pop("roles")
        hero = Hero(**h)
        if actor_name and actor_name in actor_map:
            hero.actor = actor_map[actor_name]
        for r in role_names:
            hero.roles.append(get_or_create_role(db, r))
        db.add(hero)

    db.commit()


# ─── Read Operations ──────────────────────────────────────────────────────────

def get_heroes(
    db: Session,
    attribute: Optional[str] = None,
    role: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[Hero]:
    query = db.query(Hero)
    if attribute:
        query = query.filter(Hero.attribute == attribute.lower())
    if role:
        query = query.join(Hero.roles).filter(Role.name == role.lower())
    return query.offset(skip).limit(limit).all()


def get_hero(db: Session, hero_id: int) -> Optional[Hero]:
    return db.query(Hero).filter(Hero.id == hero_id).first()


def get_hero_by_name(db: Session, name: str) -> Optional[Hero]:
    return db.query(Hero).filter(Hero.name.ilike(f"%{name}%")).first()


def get_actors(db: Session, skip: int = 0, limit: int = 100) -> List[Actor]:
    return db.query(Actor).offset(skip).limit(limit).all()


def get_actor(db: Session, actor_id: int) -> Optional[Actor]:
    return db.query(Actor).filter(Actor.id == actor_id).first()


def get_heroes_by_actor(db: Session, actor_id: int) -> List[Hero]:
    return db.query(Hero).filter(Hero.actor_id == actor_id).all()
