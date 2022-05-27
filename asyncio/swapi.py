import aiohttp
import asyncio
from sqlalchemy import  Integer, String, Column, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import config


engine = create_async_engine(config.PG_DSN_ALC, echo=True)
Base = declarative_base()
URL = 'https://swapi.dev/api/people/'

MAX = 10


class Character(Base):

    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), index=True)
    birth_year = Column(String(128))
    eye_color = Column(String(128))
    films = Column(Text)
    gender = Column(String(128))
    hair_color = Column(String(128))
    height = Column(String(128))
    homeworld = Column(String(128))
    mass = Column(String(128))
    skin_color = Column(String(128))
    species = Column(Text)
    starships = Column(Text)
    vehicles = Column(Text)

    def __repr__(self):
        return "<Character(id='%s', name='%s', birth_year='%s', eye_color='%s', films='%s', gender='%s', " \
               "hair_color='%s', height='%s', homeworld='%s', mass='%s', skin_color='%s', species='%s', " \
               "starships='%s', vehicles='%s')>" % (self.id, self.name, self.birth_year, self.eye_color, self.films,
                                                    self.gender, self.hair_color, self.height, self.homeworld,
                                                    self.mass, self.skin_color, self.species, self.starships, self.vehicles)


async def get_async_session(
    drop: bool = False, create: bool = False
):

    async with engine.begin() as conn:
        if drop:
            await conn.run_sync(Base.metadata.drop_all)
        if create:
            print(1)
            await conn.run_sync(Base.metadata.create_all)
    async_session_maker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


async def get_person(person_id, session):
    async with session.get(f'{URL}{person_id}') as response:
        return await response.json()


async def load_chars(list_of_characters, session):
    async with session.begin() as conn:
        for character in list_of_characters:
            name = character['name']
            birth_year = character['birth_year']
            eye_color = character['eye_color']
            films = str(character['films'])
            gender = character['gender']
            hair_color = character['hair_color']
            height = character['height']
            homeworld = character['homeworld']
            mass = character['mass']
            skin_color = character['skin_color']
            species = str(character['species'])
            starships = str(character['starships'])
            vehicles = str(character['vehicles'])
            character_data = Character(name=name, birth_year=birth_year, eye_color=eye_color, films=films,
                                       gender=gender, hair_color=hair_color, height=height, homeworld=homeworld,
                                       mass=mass, skin_color=skin_color, species=species, starships=starships,
                                       vehicles=vehicles)
            conn.add(character_data)


async def main():
    session = aiohttp.ClientSession()
    coros = []
    for item in range(1, MAX+1):
        coroutine = get_person(item, session)
        coros.append(coroutine)
    people = await asyncio.gather(*coros)
    for person in people:
        print(person['name'])
    await session.close()
    session_db = await get_async_session()
    await load_chars(people, session_db)
    # await session_db.close_all()



if __name__ == '__main__':
    asyncio.run(main())