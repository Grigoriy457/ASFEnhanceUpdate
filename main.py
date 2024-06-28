import asyncio

import config
from main_logger import get_logger
from asf_api import AsfApi
from steam_api import SteamApi


logger = get_logger("main")


async def process(asf_host):
    asf_api = AsfApi(asf_host)
    bots = await asf_api.get_bots()
    online_bots_count = len([bot for bot in bots if bot.is_enabled])

    await asf_api.explorer()
    logger.info(f"[+] Explore ASF {asf_host} done")
    await asyncio.sleep(30)
    await asf_api.loot()
    logger.info(f"[+] Loot ASF {asf_host} done")

    return online_bots_count


async def main(attempt=1):
    logger.info("[/] Starting processes...")
    online_bots_count = sum(await asyncio.gather(*[process(asf_host) for asf_host in config.ASF_HOSTS]))
    logger.info("[+] All processes done")

    steam_api = SteamApi()
    items = await steam_api.get_inventory()
    if len(items) < online_bots_count and attempt < config.MAX_ATTEMPTS:
        logger.warning("[!] Not enough items for selling")
        return False

    for i, item in enumerate(items, start=1):
        await steam_api.sell_item(asset_id=item.asset_id, price=1)
        logger.info(f"[+] #{i}/{len(items)} Item sold: {item.name}")
    return True


def starter():
    for attempt in range(1, config.MAX_ATTEMPTS + 1):
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        status = loop.run_until_complete(main(attempt=attempt))
        if status:
            break


if __name__ == "__main__":
    starter()
