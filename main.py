import asyncio

import config
from main_logger import get_logger
from asf_api import AsfApi


logger = get_logger("main")


async def process(asf_host):
    asf_api = AsfApi(asf_host)
    await asf_api.explorer()
    logger.info(f"Explore ASF {asf_host} done")
    await asyncio.sleep(30)
    await asf_api.loot()
    logger.info(f"ASF {asf_host} done")


async def main():
    logger.info("Starting processes...")
    await asyncio.gather(*[process(asf_host) for asf_host in config.ASF_HOSTS])


if __name__ == "__main__":
    asyncio.run(main())
