import asyncio

from patterns.facade.schedule_facade import ScheduleFacade

async def main():
    facade = ScheduleFacade()
    await facade.start_background_monitoring()
    await facade.start_bot()


if __name__ == "__main__":
    asyncio.run(main())