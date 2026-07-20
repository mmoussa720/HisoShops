import sys
from src.infrastructure.database.session import create_tables
async def setup_initial_data()->None:
    try:
        await create_tables()
    except Exception as e:
        sys.exit(1)

