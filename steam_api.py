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


class SteamException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class SteamApi:
    def __init__(self):
        self.app_id = APP_ID
        self.context_id = CONTEXT_ID

        self.steam_id = config.STEAM_ID
        self.session_id = config.STEAM_SESSION_ID
        self.login_secure = config.STEAM_LOGIN_SECURE

        self.base_url = 'https://steamcommunity.com'

    async def get_inventory(self):
        def is_card(tags):
            return dict([(tag["category"], tag["internal_name"]) for tag in tags]).get("item_class") == "item_class_2"

        params = {
            "l": "russian",
            "count": "2000"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/inventory/{self.steam_id}/{self.app_id}/{self.context_id}", params=params) as response:
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

    async def sell_item(self, asset_id: str, price: int):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"sessionid={self.session_id}; steamLoginSecure={self.login_secure}",
            "Referer": f"https://steamcommunity.com/profiles/{self.steam_id}/inventory"
        }
        data = {
            "sessionid": self.session_id,
            "appid": self.app_id,
            "contextid": self.context_id,
            "assetid": asset_id,
            "amount": 1,
            "price": price
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/market/sellitem", headers=headers, data=aiohttp.FormData(data)) as response:
                data = await response.json()
                if not data["success"]:
                    raise SteamException(f"Error in sell item: {data['message']}")


async def test():
    steam_api = SteamApi()
    steam_api.app_id = "2923300"
    steam_api.context_id = "2"
    await steam_api.sell_item("4855525049031940705", 2)


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test())
