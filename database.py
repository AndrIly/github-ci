from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

url = "sqlite+aiosqlite:///./app.db"

engine = create_async_engine(url, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()
