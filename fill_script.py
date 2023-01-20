import random
import string
import asyncio
import json
from httpx import AsyncClient


CHARACTERS = string.ascii_letters + string.digits
COROUTINES_NUM = 10
ITTERATION_PER_COROUTINE = 100_000 // COROUTINES_NUM
PERCENT_COUNT = ITTERATION_PER_COROUTINE // (100 // COROUTINES_NUM)


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
            if n_iteration % PERCENT_COUNT == 0:
                print(f"{n_iteration=}, {100 * n_iteration // ITTERATION_PER_COROUTINE}% completed")


async def main():
    await asyncio.gather(*[create_requests() for _ in range(COROUTINES_NUM)])


if __name__ == "__main__":
    asyncio.run(main())
