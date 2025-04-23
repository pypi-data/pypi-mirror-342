import asyncio

from acp_sdk.client import Client
from acp_sdk.models import (
    Message,
    MessagePart,
)


async def example() -> None:
    async with Client(base_url="http://localhost:8000") as client:
        run = await client.run_sync(agent="echo", inputs=[Message(parts=[MessagePart(content="Howdy!")])])
        print(run)


if __name__ == "__main__":
    asyncio.run(example())
