import asyncio
import json

from mcpeureka.main import get_all_services


async def amain():
    res = await get_all_services("http://172.31.241.185:8600", auth={
        "username": "devInteg",
        "password": "123456",
    })
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    asyncio.run(amain())
