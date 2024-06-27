import aiohttp
import json

import config


class AsfApi:
    def __init__(self, host):
        self.base_api_url = f"http://{host}/Api"
        self.password = config.ASF_PASSWORD

    async def execute_command(self, command):
        headers = {
            "accept": "application/json",
            "Authentication": self.password,
            "Content-Type": "application/json"
        }
        data = {
            "Command": command
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_api_url}/Command", headers=headers, data=json.dumps(data)) as response:
                return await response.json()


async def test():
    asf_api = AsfApi("10.10.10.57:80")
    print(await asf_api.execute_command("explorer asf"))


if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
