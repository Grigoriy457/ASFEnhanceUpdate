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
    instance_id: int


class SteamApi:
    def __init__(self):
        self.session_id = config.STEAM_SESSION_ID
        self.base_url = 'https://steamcommunity.com'

    async def get_inventory(self, steam_id):
        def is_card(tags):
            return dict([(tag["category"], tag["internal_name"]) for tag in tags]).get("item_class") == "item_class_2"

        params = {
            "l": "russian",
            "count": "2000"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/inventory/{steam_id}/{APP_ID}/{CONTEXT_ID}", params=params) as response:
                data = await response.json()
                descriptions = dict([(description["instanceid"], description) for description in data["descriptions"]])
                items = []
                for item in data["assets"]:
                    steam_item = SteamItem(name=descriptions[item["instanceid"]]["name"], instance_id=item["instanceid"])
                    if steam_item in items:
                        continue
                    if is_card(descriptions[item["instanceid"]]["tags"]) and descriptions[item["instanceid"]]["marketable"]:
                        items.append(steam_item)

                return items

    async def sell_item(self, asset_id, price):
        data = {
            "sessionid": self.session_id,
            "appid": APP_ID,
            "contextid": CONTEXT_ID,
            "assetid": asset_id,
            "amount": 1,
            "price": price
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
