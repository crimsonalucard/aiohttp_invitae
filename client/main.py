from aiohttp import ClientSession
import asyncio
# client code

#IO
async def fetch(session: ClientSession, url: str) -> str:
    # with async_timeout.timeout(10):
    async with session.get(url) as response:
        return await response.text()

#IO
async def main() -> None:
    async with ClientSession() as session:
        html = await fetch(session, 'http://python.org')
        print(html)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())