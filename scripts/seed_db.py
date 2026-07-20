import asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.dependencies import AsyncSessionDep
from src.infrastructure.database.session import local_session
from src.modules.users.schemas import UserCreate
from src.modules.users.services import UserService

fake = Faker()


async def seed_db():
    service = UserService()
    async with local_session() as db:
        for _ in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            user_data = UserCreate(
                first_name=first_name,
                last_name=last_name,
                user_name=fake.user_name()[:20],
                email=fake.unique.email(),
                password="Password#123",
            )
            try:
                result = await service.create_user(user_data, db)
                print(f"Created user: {result['user_name']}")
            except Exception as e:
                await db.rollback()
                print(f"Skipped user: {e}")
    print("Seeding complete.")


if __name__ == "__main__":
    asyncio.run(seed_db())
