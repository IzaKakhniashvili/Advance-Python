import aiohttp
import asyncio
import ssl
import json
import time

posts = []

async def get_post(session, i):
    url = f"https://jsonplaceholder.typicode.com/posts/{i + 1}"
    async with session.get(url, ssl=False) as response:  
        if response.status == 200:
            data = await response.json()
            posts.append(data)
        else:
            print(f"Error: {response.status}")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [get_post(session, i) for i in range(77)]
        await asyncio.gather(*tasks)

start_time = time.time()


asyncio.run(main())


with open('posts.json', 'w') as f:
    json.dump(posts, f, indent=4)

print(f"End time: {time.time() - start_time}")