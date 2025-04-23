import pytest
from aresponses import ResponsesMockServer

from aioscrapper import AIOScrapper
from aioscrapper.scrapper.base import BaseScrapper
from aioscrapper.types import Response, RequestSender


class Scrapper(BaseScrapper):
    def __init__(self):
        self.response_data = None

    async def start(self, send_request: RequestSender) -> None:
        await send_request(url="https://api.test.com/v1", callback=self.parse)

    async def parse(self, response: Response) -> None:
        self.response_data = response.json()


@pytest.mark.asyncio
async def test_success(aresponses: ResponsesMockServer):
    aresponses.add("api.test.com", "/v1", "GET", response={"status": "OK"})  # pyright: ignore

    scrapper = Scrapper()
    async with AIOScrapper(scrappers=[scrapper]) as executor:
        await executor.start()

    assert scrapper.response_data == {"status": "OK"}
    aresponses.assert_plan_strictly_followed()
