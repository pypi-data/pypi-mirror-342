# Parser FNS

## Пример работы

```python
import asyncio

from novikovtv_parser_fns.parser.models.search import SearchResult
from novikovtv_parser_fns.parser.nalog import NalogParser


async def main():
    parser = NalogParser()
    res: list[SearchResult] = await parser.search("Тест")


if __name__ == '__main__':
    asyncio.run(main())
```