import asyncio

from telegram.ext import ApplicationBuilder

from global_config import token
from patterns.facade.schedule_facade import ScheduleFacade


async def main():
    app = ApplicationBuilder().token(token).build()
    facade = ScheduleFacade(app)
    await facade.start_background_monitoring()
    await facade.start_bot()


if __name__ == "__main__":
    asyncio.run(main())
