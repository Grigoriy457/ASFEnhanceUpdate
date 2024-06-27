import aiohttp
import json
from dataclasses import dataclass

import config


@dataclass
class ExecuteCommand:
    status_code: int
    success: bool
    result: str
    message: str


class ASFError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


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
                if response.status in (500, 503):
                    raise ASFError(f"ASF is not available. Status code: {response.status} (command={command})")

                data = await response.json()
                return ExecuteCommand(
                    status_code=response.status,
                    success=data["Success"],
                    result=data["Result"],
                    message=data["Message"]
                )

    async def explorer(self):
        ret = await self.execute_command("explorer ASF")
        if not ret.success:
            raise ASFError(f"ASF explorer error: {ret.result}")

    async def loot(self):
        ret = await self.execute_command("loot ASF")
        if not ret.success:
            raise ASFError(f"ASF loot error: {ret.result}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
