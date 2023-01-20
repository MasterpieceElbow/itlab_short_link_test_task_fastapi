import random
import string
import asyncio
import json
from httpx import AsyncClient


CHARACTERS = string.ascii_letters + string.digits
COROUTINS_NUM = 20
ITTERATION_PER_COROUTINE = 1_000_000 // COROUTINS_NUM


def create_salt() -> str:
    return "".join(random.sample(CHARACTERS, k=11))


async def create_requests():
    async with AsyncClient() as client:
        for n_iteration in range(ITTERATION_PER_COROUTINE):
            await client.post(
                "http://127.0.0.1:8000/links/", 
                data=json.dumps({
                    "destination_url": f"https://www.youtube.com/watch?v={create_salt()}",
                    "days_to_expire": 90,
                }),
            )
            if n_iteration % 1000 == 0:
                print(f"{100 * n_iteration // ITTERATION_PER_COROUTINE}% completed")


async def main():
    await asyncio.gather(*[create_requests() for _ in range(COROUTINS_NUM)])


asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
