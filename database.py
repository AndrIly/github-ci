from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import declarative_base


url = "sqlite+aiosqlite:///./app.db"

engine = create_async_engine(url, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()