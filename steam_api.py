import aiohttp
from dataclasses import dataclass
from typing import List

import config


APP_ID = "753"
CONTEXT_ID = "6"


@dataclass
class SteamItem:
    name: str
    market_hash_name: str
    asset_id: str


@dataclass
class SellItem:
    requires_confirmation: bool
    success: bool


class SteamException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class SteamApi:
    def __init__(self):
        self.app_id = APP_ID
        self.context_id = CONTEXT_ID
        self.price_offset = config.PRICE_OFFSET

        self.steam_id = config.STEAM_ID
        self.session_id = config.STEAM_SESSION_ID
        self.login_secure = config.STEAM_LOGIN_SECURE

        self.base_url = 'https://steamcommunity.com'
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"sessionid={self.session_id}; steamLoginSecure={self.login_secure}; steamCountry=RU%7C9c73d4b94187f68d6431b1ba5e41bc79; strInventoryLastContext=753_0; tsTradeOffersLastRead=1719680989",
            "DNT": "1",
            "Host": "steamcommunity.com",
            "Origin": "https://steamcommunity.com",
            "Referer": f"https://steamcommunity.com/profiles/{self.steam_id}/inventory",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    async def get_inventory(self) -> List[SteamItem]:
        def is_card(tags):
            return dict([(tag["category"], tag["internal_name"]) for tag in tags]).get("item_class") == "item_class_2"

        params = {
            "l": "russian",
            "count": "2000"
        }
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(f"{self.base_url}/inventory/{self.steam_id}/{self.app_id}/{self.context_id}", params=params) as response:
                data = await response.json()
                descriptions = dict([(description["instanceid"], description) for description in data["descriptions"]])
                items = []
                for item in data["assets"]:
                    steam_item = SteamItem(name=descriptions[item["instanceid"]]["name"],
                                           market_hash_name=descriptions[item["instanceid"]]["market_hash_name"],
                                           asset_id=item["assetid"])
                    if steam_item in items:
                        continue
                    if is_card(descriptions[item["instanceid"]]["tags"]) and descriptions[item["instanceid"]]["marketable"]:
                        items.append(steam_item)
                return items

    async def sell_item(self, asset_id: str, price: int) -> SellItem:
        data = {
            "sessionid": self.session_id,
            "appid": self.app_id,
            "contextid": self.context_id,
            "assetid": asset_id,
            "amount": "1",
            "price": str(price)
        }
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(f"{self.base_url}/market/sellitem/", data=aiohttp.FormData(data)) as response:
                data = await response.json()
                if not data["success"]:
                    raise SteamException(f"Error in sell item: {data['message']}")
                return SellItem(
                    requires_confirmation=bool(data["requires_confirmation"]),
                    success=data["success"]
                )

    async def get_lowest_item_price(self, market_hash_name):
        params = {
            "country": "RU",
            "currency": "5",
            "appid": self.app_id,
            "market_hash_name": market_hash_name
        }
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(f"https://steamcommunity.com/market/priceoverview/", params=params) as response:
                data = await response.json()
                return round(float(data["lowest_price"].split(" ")[0].replace(",", ".")) * 100 - self.price_offset * 100)


async def test():
    steam_api = SteamApi()
    print(await steam_api.get_inventory())
    price = await steam_api.get_lowest_item_price("2861690-Existential Seagull")
    print(await steam_api.sell_item("30465340462", price))


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test())
