import random
import string
import asyncio
from httpx import AsyncClient

from config import DOMAIN_ADDRESS


CHARACTERS = string.ascii_letters + string.digits
TOTAL_REQUESTS = 10_000
COROUTINES_NUM = 10
ITTERATION_PER_COROUTINE = TOTAL_REQUESTS // COROUTINES_NUM
PERCENT_COUNT = ITTERATION_PER_COROUTINE // (100 // COROUTINES_NUM)
ADDRESS = f"{DOMAIN_ADDRESS}links/"


def create_hash() -> str:
    return "".join(random.sample(CHARACTERS, k=11))


async def create_requests():
    async with AsyncClient() as client:
        for n_iteration in range(ITTERATION_PER_COROUTINE):
            await client.post(
                ADDRESS, 
                json={
                    "days_to_expire": 90,
                    "destination_url": f"https://www.youtube.com/watch?v={create_hash()}"
                },
            )
            if n_iteration % PERCENT_COUNT == 0:
                print(f"{n_iteration=}, {100 * n_iteration // ITTERATION_PER_COROUTINE}% completed")


async def main():
    await asyncio.gather(*[create_requests() for _ in range(COROUTINES_NUM)])


if __name__ == "__main__":
    asyncio.run(main())
