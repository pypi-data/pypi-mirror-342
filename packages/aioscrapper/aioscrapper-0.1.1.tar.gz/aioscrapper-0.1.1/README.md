# aioscrapper

**Asynchronous framework for building modular and scalable web scrapers.**

![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/github/license/darkstussy/aioscrapper)
![Version](https://img.shields.io/github/v/tag/darkstussy/aioscrapper?label=version)

## Features

- 🚀 Fully asynchronous architecture powered by `aiohttp` and `aiojobs`
- 🔧 Modular system with middleware support
- 📦 Pipeline data processing
- ⚙️ Flexible configuration
- 🔄 Priority-based request queue management
- 🛡️ Built-in error handling

## Installation

```bash
pip install aioscrapper
```

## Requirements

- Python 3.12 or higher
- aiohttp
- aiojobs

## Quick Start

```python
import asyncio

from aioscrapper import BaseScrapper, AIOScrapper, RequestSender
from aioscrapper.types import Response


class Scrapper(BaseScrapper):
    async def start(self, request_sender: RequestSender) -> None:
        await request_sender(url="https://example.com", callback=self.parse)

    async def parse(self, response: Response) -> None:
        # handle response
        pass


async def main():
    async with AIOScrapper(scrappers=[Scrapper()]) as scrapper:
        await scrapper.start()


if __name__ == "__main__":
    asyncio.run(main())
```

## License

MIT License

Copyright (c) 2025 darkstussy

## Links

- [PyPI](https://pypi.org/project/aioscrapper)
- [GitHub](https://github.com/darkstussy/aioscrapper)
- [Issues](https://github.com/darkstussy/aioscrapper/issues)