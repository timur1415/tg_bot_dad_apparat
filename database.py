from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_async_engine(os.getenv("DATABASE_URL"), echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session