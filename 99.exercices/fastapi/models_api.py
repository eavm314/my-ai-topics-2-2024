from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from datetime import datetime
from enum import Enum
import uuid

class RaceEnum(str, Enum):
    elf="ELF"
    human='HUMAN'
    orc='ORC'

class Guild(BaseModel):
    id: str = None
    name: str
    realm: str
    created: datetime = None

class Character(BaseModel):
    id: str = None
    name: str
    level: int
    race: RaceEnum
    hp: int
    damage: int
    guild: Guild

class CharacterCreate(BaseModel):
    name: str
    level: int
    race: RaceEnum
    hp: int
    damage: int
    guildId: str

class CharacterUpdate(BaseModel):
    name: str = None
    level: int = None
    race: RaceEnum = None
    hp: int = None
    damage: int = None
    guildId: str = None

app = FastAPI(title='Validation Api')

guilds = {}
characters = {}

@app.post("/guilds", status_code=201)
def create_guild(guild: Guild):
    id = uuid.uuid4()
    guild.id = id
    guild.created = datetime.now()
    guilds[str(id)] = guild
    return guild

@app.post("/characters", status_code=201)
def create_character(created_character: CharacterCreate):
    print(guilds.keys())
    if created_character.guildId not in guilds.keys():
        raise HTTPException(status_code=404, detail="Guild not found")
    id = uuid.uuid4()
    character = Character(
        name=created_character.name,
        level=created_character.level,
        race=created_character.race,
        hp=created_character.hp,
        damage=created_character.damage,
        guild=guilds[created_character.guildId]
    )
    character.id = id
    characters[str(id)] = character
    return character

@app.get("/guilds")
def get_guilds():
    return list(guilds.values())

@app.get("/characters")
def get_characters():
    return characters

@app.patch("/characters/{id}")
def update_character(id: str, update_character: CharacterUpdate):
    if id not in characters.keys():
        raise HTTPException(status_code=404, detail="Character not found")
    character = characters[id]

    for field, value in dict(update_character).items():
        if field == 'guildId' and value is not None:
            if value not in guilds.keys():
                raise HTTPException(status_code=404, detail="Guild not found")
            field = 'guild'
            value = guilds[value]
        if value is not None:
            setattr(character, field, value)

    characters[id] = character
    return character

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("models_api:app", reload=True, port=8008)