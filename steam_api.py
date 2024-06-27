import aiohttp
import json
from dataclasses import dataclass
from pprint import pprint

import config


APP_ID = "753"
CONTEXT_ID = "6"


@dataclass
class SteamItem:
    name: str
    market_hash_name: str


class SteamApi:
    def __init__(self):
        self.session_id = config.STEAM_SESSION_ID
        self.base_url = 'https://steamcommunity.com'

    async def get_inventory(self, steam_id):
        def is_card(tags):
            return "item_class" in [tag["category"] for tag in tags]

        params = {
            "l": "russian",
            "count": "2000"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/inventory/{steam_id}/{APP_ID}/{CONTEXT_ID}", params=params) as response:
                data = await response.json()
                items = [
                    SteamItem(name=item["name"], market_hash_name=item["market_hash_name"])
                    for item in data["descriptions"]
                    if is_card(item["tags"]) and item["marketable"]
                ]
                return items

    async def sell_item(self):
        data = {
            "sessionid": self.session_id,
            "appid": APP_ID,
            "contextid": CONTEXT_ID,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/market/sellitem", data=json.dumps(data)) as response:
                return await response.json()


async def test():
    steam_api = SteamApi()
    pprint(await steam_api.get_inventory("76561199205197880"))


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test())
